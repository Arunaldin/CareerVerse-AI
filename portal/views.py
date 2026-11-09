import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone

from .forms import StudentForm, StudentProfileForm
from .models import (
    Student, StudentProfile, AptitudeQuestion, QuizAttempt,
    CodingProblem, CodingSubmission, CompanyPlacement,
    SavedResume, CareerGuidanceResult, InterviewPracticeSession,
    StudentMembership, DailyGoal,
    # CS Learning Hub
    Subject, Topic, TopicQuiz, LearningPath, LearningPathStep,
    StudentLearningProgress, StudentPathEnrollment
)
from .ai_service import (
    generate_career_guidance,
    generate_interview_questions,
    evaluate_interview_answer
)
from .code_runner import execute_python_code, execute_code_multi_language


# -----------------------------------------------------------------------------
# LANDING & PUBLIC PAGES
# -----------------------------------------------------------------------------

def home(request):
    """Modern SaaS landing page"""
    companies = CompanyPlacement.objects.all()[:6]
    problems_count = CodingProblem.objects.count()
    questions_count = AptitudeQuestion.objects.count()

    context = {
        'companies': companies,
        'problems_count': problems_count,
        'questions_count': questions_count,
    }
    return render(request, 'home.html', context)


def about(request):
    """About CareerVerse AI"""
    return render(request, 'about.html')


def contact(request):
    """Contact & support view"""
    if request.method == 'POST':
        messages.success(request, "Thank you! Your message has been received. Our team will get back to you shortly.")
        return render(request, 'contact.html', {'success': True})
    return render(request, 'contact.html')


# -----------------------------------------------------------------------------
# AUTHENTICATION & PROFILE
# -----------------------------------------------------------------------------

def register(request):
    """Student registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Create User
            user = User.objects.create_user(
                username=username,
                email=student.email,
                password=password,
                first_name=student.name
            )

            student.save()

            # Auto-create empty StudentProfile
            StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    'college': 'University / College',
                    'department': 'Computer Science & Engineering',
                    'cgpa': 7.50,
                    'graduation_year': 2026,
                    'skills': 'Python, SQL, Problem Solving',
                    'interests': 'Software Development, AI'
                }
            )

            # Auto-login after registration
            login(request, user)
            messages.success(request, f"Welcome to CareerVerse AI, {username}! Your journey starts here.")
            return redirect('dashboard')
    else:
        form = StudentForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Student login"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'dashboard')
        else:
            error = 'Invalid username or password. Please check your credentials.'

    return render(request, 'login.html', {'error': error})


def logout_view(request):
    """User logout"""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def profile(request):
    """Student profile view and update"""
    profile_obj, created = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'college': 'College of Engineering',
            'department': 'Computer Science',
            'cgpa': 7.50,
            'graduation_year': 2026,
            'skills': 'Python, SQL, HTML, CSS',
            'interests': 'Software Engineering'
        }
    )

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile_obj)
        # Also allow updating user's full name and email
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')

        if form.is_valid():
            if full_name:
                request.user.first_name = full_name
            if email:
                request.user.email = email
            request.user.save()

            profile_saved = form.save(commit=False)
            profile_saved.user = request.user
            profile_saved.save()

            messages.success(request, "Your profile has been updated successfully! ✨")
            return redirect('profile')
    else:
        form = StudentProfileForm(instance=profile_obj)

    completion = profile_obj.completion_percentage()
    recent_quizzes = QuizAttempt.objects.filter(user=request.user).order_by('-created_at')[:3]
    recent_codes = CodingSubmission.objects.filter(user=request.user).order_by('-created_at')[:3]

    return render(request, 'profile.html', {
        'form': form,
        'profile': profile_obj,
        'completion': completion,
        'recent_quizzes': recent_quizzes,
        'recent_codes': recent_codes,
    })


@login_required
def change_password(request):
    """Password management"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


# -----------------------------------------------------------------------------
# STUDENT DASHBOARD
# -----------------------------------------------------------------------------

@login_required
def dashboard(request):
    """Personalized Student Dashboard with analytics, streak and daily goals"""
    user = request.user
    profile_obj, _ = StudentProfile.objects.get_or_create(
        user=user,
        defaults={
            'college': 'University / College',
            'department': 'Computer Science & Engineering',
            'cgpa': 7.50,
            'graduation_year': 2026,
            'skills': 'Python, SQL, Web Basics',
            'interests': 'Software Development'
        }
    )

    # Update student learning streak
    profile_obj.update_streak()

    # Daily Goals tracking
    today = timezone.now().date()
    today_goal, _ = DailyGoal.objects.get_or_create(
        user=user,
        date=today,
        defaults={
            'target_coding': 2,
            'target_aptitude': 5,
            'target_topics': 1,
            'target_interviews': 1
        }
    )
    daily_stats = today_goal.completion_stats()

    # Statistics calculation
    quiz_attempts = QuizAttempt.objects.filter(user=user)
    total_quizzes = quiz_attempts.count()
    avg_accuracy = round(sum(q.accuracy for q in quiz_attempts) / total_quizzes, 1) if total_quizzes > 0 else 0

    coding_submissions = CodingSubmission.objects.filter(user=user)
    solved_problems_count = coding_submissions.filter(status='Passed').values('problem').distinct().count()
    total_problems = CodingProblem.objects.count()

    topics_completed_count = StudentLearningProgress.objects.filter(user=user, is_completed=True).count()
    interview_count = InterviewPracticeSession.objects.filter(user=user).count()
    resumes_count = SavedResume.objects.filter(user=user).count()

    # Overall Placement Readiness Score (0-100)
    profile_comp = profile_obj.completion_percentage()
    coding_score = min(int((solved_problems_count / max(total_problems, 1)) * 100), 100)
    aptitude_score = int(avg_accuracy)
    interview_score = min(interview_count * 25, 100)

    readiness_score = int(
        (profile_comp * 0.25) +
        (aptitude_score * 0.25) +
        (coding_score * 0.30) +
        (interview_score * 0.20)
    )

    # Recommended Learning Path
    skills_list = [s.strip().lower() for s in (profile_obj.skills or '').split(',') if s.strip()]
    recommendations = []
    if 'python' not in skills_list:
        recommendations.append({
            'title': 'Master Python Fundamentals',
            'desc': 'Core language for technical interviews & AI engineering.',
            'category': 'Coding',
            'link': '/coding/'
        })
    if 'sql' not in skills_list:
        recommendations.append({
            'title': 'Learn Relational SQL Queries',
            'desc': 'Crucial for database rounds in TCS, Infosys, and Amazon.',
            'category': 'Database',
            'link': '/coding/'
        })
    recommendations.append({
        'title': 'Quantitative Aptitude Speed Test',
        'desc': 'Solve 10 timed questions on Percentages & Time-Work.',
        'category': 'Aptitude',
        'link': '/aptitude/'
    })
    recommendations.append({
        'title': 'Practice AI Mock Interview',
        'desc': 'Simulate real-time technical & HR rounds with instant feedback.',
        'category': 'Interview',
        'link': '/interview/'
    })

    recent_attempts = quiz_attempts.order_by('-created_at')[:5]
    top_companies = CompanyPlacement.objects.all()[:4]

    context = {
        'profile': profile_obj,
        'profile_comp': profile_comp,
        'current_streak': profile_obj.current_streak,
        'longest_streak': profile_obj.longest_streak,
        'today_goal': today_goal,
        'daily_stats': daily_stats,
        'total_quizzes': total_quizzes,
        'avg_accuracy': avg_accuracy,
        'solved_problems_count': solved_problems_count,
        'total_problems': total_problems,
        'topics_completed_count': topics_completed_count,
        'interview_count': interview_count,
        'resumes_count': resumes_count,
        'readiness_score': readiness_score,
        'recommendations': recommendations[:3],
        'recent_attempts': recent_attempts,
        'top_companies': top_companies,
    }
    return render(request, 'dashboard.html', context)


# -----------------------------------------------------------------------------
# AI CAREER GUIDANCE
# -----------------------------------------------------------------------------

def career_guidance(request):
    """Feature 6: AI-Powered Career Guidance & Personalized Career Recommendations Engine"""
    user_profile = None
    solved_count = 0
    avg_accuracy = 0

    if request.user.is_authenticated:
        user_profile, _ = StudentProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'college': 'University / College',
                'department': 'Computer Science & Engineering',
                'cgpa': 7.50,
                'graduation_year': 2026,
                'skills': 'Python, SQL, Web Basics',
                'interests': 'Software Development'
            }
        )
        solved_count = CodingSubmission.objects.filter(user=request.user, status='Passed').values('problem').distinct().count()
        attempts = QuizAttempt.objects.filter(user=request.user)
        if attempts.exists():
            avg_accuracy = round(sum(a.accuracy for a in attempts) / attempts.count(), 1)

    personalized_tracks = []
    if user_profile:
        personalized_tracks = _generate_personalized_recommendations(user_profile, solved_count, avg_accuracy)

    if request.method == "POST":
        degree = request.POST.get("degree", "").strip()
        cgpa = request.POST.get("cgpa", "").strip()
        skills = request.POST.get("skills", "").strip()
        interests = request.POST.get("interests", "").strip()

        # Update profile with latest inputs if authenticated
        if request.user.is_authenticated and user_profile:
            if skills:
                user_profile.skills = skills
            if interests:
                user_profile.interests = interests
            user_profile.save()
            user_profile.update_streak()
            personalized_tracks = _generate_personalized_recommendations(user_profile, solved_count, avg_accuracy)

        # Generate guidance via AI service
        ai_result = generate_career_guidance(degree, cgpa, skills, interests)

        # Save to database if user is logged in
        if request.user.is_authenticated:
            CareerGuidanceResult.objects.create(
                user=request.user,
                degree=degree,
                cgpa=cgpa,
                skills=skills,
                interests=interests,
                ai_result=ai_result
            )

        return render(request, "career_result.html", {
            "degree": degree,
            "cgpa": cgpa,
            "skills": skills,
            "interests": interests,
            "ai_result": ai_result,
            "personalized_tracks": personalized_tracks
        })

    return render(request, "career_guidance.html", {
        'profile': user_profile,
        'personalized_tracks': personalized_tracks,
        'solved_count': solved_count,
        'avg_accuracy': avg_accuracy
    })


# -----------------------------------------------------------------------------
# RESUME BUILDER
# -----------------------------------------------------------------------------

def resume(request):
    """Resume Builder with template choices and instant live preview"""
    user_profile = None
    if request.user.is_authenticated:
        user_profile, _ = StudentProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'college': 'University / College',
                'department': 'Computer Science & Engineering',
                'cgpa': 7.50,
                'graduation_year': 2026,
                'skills': 'Python, SQL, Web Basics',
                'interests': 'Software Development'
            }
        )

    if request.method == "POST":
        data = {
            "name": request.POST.get("name", ""),
            "email": request.POST.get("email", ""),
            "phone": request.POST.get("phone", ""),
            "objective": request.POST.get("objective", ""),
            "education": request.POST.get("education", ""),
            "skills": request.POST.get("skills", ""),
            "projects": request.POST.get("projects", ""),
            "experience": request.POST.get("experience", ""),
            "certifications": request.POST.get("certifications", ""),
            "template": request.POST.get("template", "modern"),
        }

        # Save resume to database if authenticated
        if request.user.is_authenticated:
            SavedResume.objects.update_or_create(
                user=request.user,
                title=f"{data['name']} - Resume",
                defaults={
                    'template_name': data['template'],
                    'resume_data': data
                }
            )

        return render(request, "generated_resume.html", data)

    return render(request, "resume.html", {
        'profile': user_profile
    })


# -----------------------------------------------------------------------------
# APTITUDE PREPARATION & QUIZZES
# -----------------------------------------------------------------------------

def aptitude(request):
    """Aptitude practice and timed tests"""
    category = request.GET.get('category', 'all')
    difficulty = request.GET.get('difficulty', 'all')

    questions_qs = AptitudeQuestion.objects.all()
    if category != 'all':
        questions_qs = questions_qs.filter(category=category)
    if difficulty != 'all':
        questions_qs = questions_qs.filter(difficulty=difficulty)

    if request.method == "POST":
        score = 0
        total = 0
        user_answers = {}

        # Evaluate submitted questions
        for key, val in request.POST.items():
            if key.startswith('q_'):
                q_id = key.replace('q_', '')
                try:
                    q_obj = AptitudeQuestion.objects.get(id=q_id)
                    total += 1
                    user_answers[q_id] = val
                    if val.strip().upper() == q_obj.correct_option.strip().upper():
                        score += 1
                except AptitudeQuestion.DoesNotExist:
                    pass

        # Also support legacy q1, q2 format for backward compatibility
        if total == 0:
            legacy_answers = {"q1": "30", "q2": "30", "q3": "20"}
            for q_key, correct_val in legacy_answers.items():
                if request.POST.get(q_key) == correct_val:
                    score += 1
                total += 1

        accuracy = round((score / total) * 100, 1) if total > 0 else 0

        # Save attempt if authenticated
        if request.user.is_authenticated:
            QuizAttempt.objects.create(
                user=request.user,
                category=category.title(),
                score=score,
                total_questions=total,
                accuracy=accuracy
            )

        return render(request, "aptitude_result.html", {
            "score": score,
            "total": total,
            "accuracy": accuracy,
            "category": category.title(),
        })

    questions = list(questions_qs[:15])

    return render(request, "aptitude.html", {
        "questions": questions,
        "selected_category": category,
        "selected_difficulty": difficulty,
        "total_count": questions_qs.count()
    })


def quiz(request):
    """General Placement Aptitude & Technical Quiz"""
    if request.method == "POST":
        answers = {
            "q1": "5",
            "q2": "Python",
            "q3": "a",
            "q4": "CSS",
            "q5": "SQLite",
            "q6": "#",
            "q7": "SELECT",
            "q8": "Hyper Text Markup Language",
            "q9": "def",
            "q10": "List"
        }

        score = 0
        for question, correct_answer in answers.items():
            if request.POST.get(question) == correct_answer:
                score += 1

        accuracy = round((score / len(answers)) * 100, 1)

        if request.user.is_authenticated:
            QuizAttempt.objects.create(
                user=request.user,
                category='Foundation Quiz',
                score=score,
                total_questions=len(answers),
                accuracy=accuracy
            )

        return render(request, "quiz_result.html", {
            "score": score,
            "total": len(answers),
            "accuracy": accuracy
        })

    return render(request, "quiz.html")


def result(request):
    """Legacy result view"""
    return render(request, 'result.html')


# -----------------------------------------------------------------------------
# CODING PREPARATION
# -----------------------------------------------------------------------------

def coding(request):
    """Coding Practice Index"""
    category = request.GET.get('category', 'all')
    difficulty = request.GET.get('difficulty', 'all')
    search = request.GET.get('search', '').strip()

    problems = CodingProblem.objects.all()
    if category != 'all':
        problems = problems.filter(category=category)
    if difficulty != 'all':
        problems = problems.filter(difficulty=difficulty)
    if search:
        problems = problems.filter(title__icontains=search)

    # Legacy POST support
    message = None
    if request.method == "POST":
        message = "Code submitted successfully! ✅ Great effort."

    # Identify solved problems for logged-in user
    solved_ids = set()
    if request.user.is_authenticated:
        solved_ids = set(
            CodingSubmission.objects.filter(user=request.user, status='Passed')
            .values_list('problem_id', flat=True)
        )

    return render(request, "coding.html", {
        "problems": problems,
        "solved_ids": solved_ids,
        "selected_category": category,
        "selected_difficulty": difficulty,
        "search": search,
        "message": message
    })


def coding_detail(request, problem_id):
    """Interactive Code Execution Workbench with Multi-Language Support"""
    problem = get_object_or_404(CodingProblem, id=problem_id)
    user_submission = None
    is_solved = False
    past_submissions = []

    if request.user.is_authenticated:
        past_submissions = list(
            CodingSubmission.objects.filter(user=request.user, problem=problem)
            .order_by('-created_at')[:5]
        )
        user_submission = past_submissions[0] if past_submissions else None
        is_solved = CodingSubmission.objects.filter(
            user=request.user, problem=problem, status='Passed'
        ).exists()

    last_lang = 'python'
    if user_submission and hasattr(user_submission, 'language') and user_submission.language:
        last_lang = user_submission.language

    return render(request, "coding_detail.html", {
        "problem": problem,
        "last_code": user_submission.code if user_submission else problem.starter_code,
        "last_language": last_lang,
        "is_solved": is_solved,
        "past_submissions": past_submissions
    })


@require_POST
def run_code_api(request):
    """AJAX API endpoint for running and submitting code across multiple programming languages"""
    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        language = data.get('language', 'python')
        custom_input = data.get('custom_input', '')
        problem_id = data.get('problem_id')
        action = data.get('action', 'run')  # 'run' or 'submit'

        problem = None
        test_cases = []
        if problem_id:
            problem = CodingProblem.objects.filter(id=problem_id).first()
            if problem and problem.test_cases:
                test_cases = problem.test_cases

        result_data = execute_code_multi_language(
            code_string=code,
            language=language,
            custom_input=custom_input,
            test_cases=test_cases
        )

        # Distinguish between Run and Submit
        total_tests = result_data.get('total_tests', 0)
        passed_count = result_data.get('passed_count', 0)
        is_pass = result_data['success'] and (passed_count >= total_tests if total_tests > 0 else True)

        status = 'Passed' if is_pass else 'Failed'
        if not result_data['success']:
            status = 'Syntax Error'

        result_data['is_submission'] = (action == 'submit')
        result_data['status'] = status

        # Save submission to database when user submits or when code passes
        if request.user.is_authenticated and problem:
            if action == 'submit' or is_pass:
                submission = CodingSubmission.objects.create(
                    user=request.user,
                    problem=problem,
                    language=language,
                    code=code,
                    status=status,
                    passed_count=passed_count,
                    total_tests=total_tests,
                    output_log=(result_data.get('output') or result_data.get('error') or '')[:2000]
                )
                result_data['submission_id'] = submission.id
                result_data['submission_time'] = submission.created_at.strftime('%H:%M:%S')

        return JsonResponse(result_data)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def technical(request):
    """Technical interview revision"""
    if request.method == "POST":
        return render(request, "technical.html", {
            "message": "Answers submitted successfully! ✅ Keep practicing."
        })
    return render(request, "technical.html")


def hr(request):
    """HR interview practice"""
    if request.method == "POST":
        return render(request, "hr.html", {
            "message": "Answers submitted successfully! ✅ Great response."
        })
    return render(request, "hr.html")


# -----------------------------------------------------------------------------
# PLACEMENT PREPARATION (COMPANY-WISE)
# -----------------------------------------------------------------------------

def placement(request):
    """Placement preparation hub with company-wise roadmaps and smart search"""
    from django.db.models import Q
    category = request.GET.get('category', 'all')
    search_query = request.GET.get('q', '').strip()

    companies = CompanyPlacement.objects.all()
    if category != 'all' and category:
        companies = companies.filter(category=category)

    if search_query:
        companies = companies.filter(
            Q(name__icontains=search_query) |
            Q(tagline__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(overview__icontains=search_query) |
            Q(eligible_branches__icontains=search_query)
        )

    return render(request, 'placement.html', {
        'companies': companies,
        'selected_category': category,
        'search_query': search_query,
        'total_count': companies.count()
    })


def company_detail(request, company_slug):
    """Company-specific placement guide and previous patterns"""
    company = get_object_or_404(CompanyPlacement, slug=company_slug)
    related_companies = CompanyPlacement.objects.exclude(id=company.id)[:3]

    return render(request, 'company_detail.html', {
        'company': company,
        'related_companies': related_companies
    })


def company_compare(request):
    """Company vs Company head-to-head comparison"""
    all_companies = CompanyPlacement.objects.all().order_by('name')
    c1_slug = request.GET.get('comp1', 'tcs')
    c2_slug = request.GET.get('comp2', 'infosys')

    comp1 = CompanyPlacement.objects.filter(slug=c1_slug).first() or all_companies.first()
    comp2 = CompanyPlacement.objects.filter(slug=c2_slug).first() or all_companies.last()

    return render(request, 'company_compare.html', {
        'all_companies': all_companies,
        'comp1': comp1,
        'comp2': comp2,
    })


# -----------------------------------------------------------------------------
# AI INTERVIEW PREPARATION
# -----------------------------------------------------------------------------

def interview(request):
    """AI-Powered Mock Interview Generator"""
    user_profile = None
    if request.user.is_authenticated:
        user_profile, _ = StudentProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'college': 'University / College',
                'department': 'Computer Science & Engineering',
                'cgpa': 7.50,
                'graduation_year': 2026,
                'skills': 'Python, SQL, Web Basics',
                'interests': 'Software Development'
            }
        )

    if request.method == "POST":
        role = request.POST.get("role", "Software Engineer").strip()
        company = request.POST.get("company", "Top Tech Company").strip()
        skills = request.POST.get("skills", "").strip()
        experience = request.POST.get("experience", "Fresher").strip()
        interview_type = request.POST.get("interview_type", "Technical").strip()

        # Call AI service
        ai_result = generate_interview_questions(role, company, skills, experience)

        session_obj = None
        if request.user.is_authenticated:
            # Update user learning streak
            if user_profile:
                user_profile.update_streak()

            # Parse questions into structured items if possible
            strengths = [
                f"Demonstrated foundational grasp of {role} fundamentals",
                "Clear, structured thought process in approaching questions",
                "Good technical alignment with target recruiter requirements"
            ]
            weaknesses = [
                "Could elaborate more on Big-O space and time complexity tradeoffs",
                "Provide more concrete metrics when describing past project challenges"
            ]
            suggestions = [
                f"Review {company} previously asked coding and technical patterns in Company Hub",
                "Practice voice recording to improve answer delivery pacing and confidence",
                "Ensure answers follow the STAR methodology (Situation, Task, Action, Result)"
            ]
            recommended_topics = [
                "Data Structures: Hash Maps & Trees",
                "DBMS: Indexing, Transactions & Normalization",
                "System Design & REST API Principles"
            ]

            session_obj = InterviewPracticeSession.objects.create(
                user=request.user,
                role=role,
                company=company,
                skills=skills,
                experience=experience,
                interview_type=interview_type,
                ai_result=ai_result,
                overall_score=78,
                technical_score=75,
                communication_score=82,
                confidence_score=76,
                strengths=strengths,
                weaknesses=weaknesses,
                improvement_suggestions=suggestions,
                recommended_topics=recommended_topics
            )

        return render(request, "interview_result.html", {
            "role": role,
            "company": company,
            "skills": skills,
            "experience": experience,
            "interview_type": interview_type,
            "ai_result": ai_result,
            "session": session_obj
        })

    return render(request, "interview.html", {
        'profile': user_profile
    })


@require_POST
def interview_evaluate(request):
    """AJAX endpoint: evaluate student's interview answer in real-time"""
    try:
        data = json.loads(request.body)
        role = data.get('role', 'Software Engineer')
        question = data.get('question', '')
        answer = data.get('answer', '')
        interview_type = data.get('interview_type', 'Technical')
        session_id = data.get('session_id')

        evaluation = evaluate_interview_answer(role, question, answer, interview_type)

        # If tied to a session, append evaluation to session history
        if session_id and request.user.is_authenticated:
            sess = InterviewPracticeSession.objects.filter(id=session_id, user=request.user).first()
            if sess:
                eval_list = sess.evaluations or []
                eval_list.append({
                    'question': question,
                    'answer': answer,
                    'score': evaluation.get('score', 75),
                    'feedback': evaluation.get('feedback', ''),
                    'strengths': evaluation.get('strengths', ''),
                    'improvements': evaluation.get('improvements', '')
                })
                sess.evaluations = eval_list
                # Recompute overall score
                scores = [e.get('score', 75) for e in eval_list if isinstance(e.get('score'), (int, float))]
                if scores:
                    sess.overall_score = int(sum(scores) / len(scores))
                sess.save()

        return JsonResponse(evaluation)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def interview_report(request, session_id):
    """Detailed Interview Performance Report with scorecards, strengths, weaknesses & study links"""
    session = get_object_or_404(InterviewPracticeSession, id=session_id)
    if request.user.is_authenticated and session.user and session.user != request.user:
        messages.error(request, "You do not have permission to view another student's report.")
        return redirect('interview')

    # Calculate performance level
    score = session.overall_score
    if score >= 85:
        level = "Placement Ready (Top Tier)"
        badge_class = "badge-success"
    elif score >= 70:
        level = "Interview Ready (Standard)"
        badge_class = "badge-primary"
    else:
        level = "Needs Additional Practice"
        badge_class = "badge-warning"

    # Default metrics if empty
    strengths = session.strengths or [
        "Strong fundamental understanding of core concepts",
        "Clear and structured verbal communication",
        "Good alignment with target role expectations"
    ]
    weaknesses = session.weaknesses or [
        "Needs deeper explanation of time and space complexity",
        "Could provide more quantified examples in STAR responses"
    ]
    suggestions = session.improvement_suggestions or [
        f"Review {session.company} company placement guide in CareerVerse",
        "Practice coding problems with strict 30-minute timer",
        "Use active verbs when explaining past projects"
    ]
    recommended_topics = session.recommended_topics or [
        "Data Structures: Trees, Graphs & Hash Tables",
        "Database: Normalization, Joins & Indexing",
        "OOP: Polymorphism, Abstract Classes vs Interfaces"
    ]

    return render(request, "interview_report.html", {
        "session": session,
        "level": level,
        "badge_class": badge_class,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "recommended_topics": recommended_topics
    })


@login_required
def interview_history(request):
    """List of all mock interview sessions and reports for the logged-in student"""
    sessions = InterviewPracticeSession.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "interview_history.html", {
        "sessions": sessions
    })


# -----------------------------------------------------------------------------
# STUDENT PROGRESS TRACKING & DAILY GOALS
# -----------------------------------------------------------------------------

@login_required
def student_progress(request):
    """Feature 1 & 2: Comprehensive Student Progress Tracker with interactive analytics"""
    user = request.user
    profile_obj, _ = StudentProfile.objects.get_or_create(
        user=user,
        defaults={
            'college': 'University / College',
            'department': 'Computer Science & Engineering',
            'cgpa': 7.50,
            'graduation_year': 2026,
            'skills': 'Python, SQL, Web Basics',
            'interests': 'Software Development'
        }
    )

    # Update streak
    profile_obj.update_streak()

    # Today's daily goal
    today = timezone.now().date()
    today_goal, _ = DailyGoal.objects.get_or_create(
        user=user,
        date=today,
        defaults={
            'target_coding': 2,
            'target_aptitude': 5,
            'target_topics': 1,
            'target_interviews': 1
        }
    )
    daily_stats = today_goal.completion_stats()

    # 1. Topic Progress Breakdown
    all_topics = Topic.objects.filter(is_active=True)
    total_topics_count = all_topics.count()
    completed_progress = StudentLearningProgress.objects.filter(user=user, is_completed=True)
    completed_topics_count = completed_progress.count()
    completed_topic_ids = set(completed_progress.values_list('topic_id', flat=True))

    subject_progress_list = []
    subjects = Subject.objects.filter(is_active=True).order_by('order')
    for subj in subjects:
        subj_topics = subj.topics.filter(is_active=True)
        s_total = subj_topics.count()
        s_done = subj_topics.filter(id__in=completed_topic_ids).count()
        pct = int((s_done / s_total) * 100) if s_total > 0 else 0
        subject_progress_list.append({
            'subject': subj,
            'total': s_total,
            'done': s_done,
            'pending': s_total - s_done,
            'percent': pct
        })

    # 2. Coding Submissions Breakdown
    coding_subs = CodingSubmission.objects.filter(user=user)
    total_submissions = coding_subs.count()
    passed_subs = coding_subs.filter(status='Passed')
    unique_solved_count = passed_subs.values('problem').distinct().count()
    total_problems_count = CodingProblem.objects.count()

    # Solved by difficulty
    easy_solved = passed_subs.filter(problem__difficulty='Easy').values('problem').distinct().count()
    medium_solved = passed_subs.filter(problem__difficulty='Medium').values('problem').distinct().count()
    hard_solved = passed_subs.filter(problem__difficulty='Hard').values('problem').distinct().count()

    # Solved by language
    lang_breakdown = {}
    for sub in passed_subs:
        l = (sub.language or 'python').lower()
        lang_breakdown[l] = lang_breakdown.get(l, 0) + 1

    # 3. Aptitude & Quiz Analytics
    quiz_attempts = QuizAttempt.objects.filter(user=user).order_by('created_at')
    total_quizzes = quiz_attempts.count()
    avg_accuracy = round(sum(q.accuracy for q in quiz_attempts) / total_quizzes, 1) if total_quizzes > 0 else 0
    accuracy_history = [
        {'date': q.created_at.strftime('%b %d'), 'accuracy': q.accuracy, 'score': q.score, 'category': q.category}
        for q in quiz_attempts[:15]
    ]

    # 4. Mock Interview Historical Scores
    interview_sessions = InterviewPracticeSession.objects.filter(user=user).order_by('-created_at')
    avg_interview_score = int(sum(s.overall_score for s in interview_sessions) / len(interview_sessions)) if interview_sessions else 0

    # 5. Chronological Student Learning History
    activity_log = []
    for q in quiz_attempts.order_by('-created_at')[:8]:
        activity_log.append({
            'type': 'Aptitude Test',
            'title': f"{q.category} Quiz ({q.score}/{q.total_questions})",
            'date': q.created_at,
            'badge': f"{q.accuracy}% Accuracy",
            'badge_class': 'badge-success' if q.accuracy >= 70 else 'badge-warning',
            'icon': '📝'
        })
    for cs in coding_subs.order_by('-created_at')[:8]:
        activity_log.append({
            'type': 'Coding Challenge',
            'title': f"{cs.problem.title} ({cs.language.upper() if cs.language else 'PYTHON'})",
            'date': cs.created_at,
            'badge': cs.status,
            'badge_class': 'badge-success' if cs.status == 'Passed' else 'badge-danger',
            'icon': '💻'
        })
    for sess in interview_sessions[:6]:
        activity_log.append({
            'type': 'AI Mock Interview',
            'title': f"{sess.role} @ {sess.company}",
            'date': sess.created_at,
            'badge': f"Score: {sess.overall_score}/100",
            'badge_class': 'badge-primary',
            'icon': '🤖'
        })
    for tp in completed_progress.order_by('-completed_at')[:8]:
        if tp.completed_at:
            activity_log.append({
                'type': 'CS Hub Topic',
                'title': f"Completed: {tp.topic.title}",
                'date': tp.completed_at,
                'badge': 'Topic Done',
                'badge_class': 'badge-success',
                'icon': '📚'
            })

    activity_log.sort(key=lambda x: x['date'], reverse=True)
    activity_log = activity_log[:20]

    # Placement Readiness Score
    profile_comp = profile_obj.completion_percentage()
    readiness_score = int(
        (profile_comp * 0.20) +
        (avg_accuracy * 0.25) +
        (min(int((unique_solved_count / max(total_problems_count, 1)) * 100), 100) * 0.35) +
        (min(interview_sessions.count() * 25, 100) * 0.20)
    )

    context = {
        'profile': profile_obj,
        'current_streak': profile_obj.current_streak,
        'longest_streak': profile_obj.longest_streak,
        'today_goal': today_goal,
        'daily_stats': daily_stats,
        'readiness_score': readiness_score,
        # Topics
        'total_topics_count': total_topics_count,
        'completed_topics_count': completed_topics_count,
        'pending_topics_count': max(0, total_topics_count - completed_topics_count),
        'topic_completion_pct': int((completed_topics_count / max(total_topics_count, 1)) * 100),
        'subject_progress_list': subject_progress_list,
        # Coding
        'total_submissions': total_submissions,
        'unique_solved_count': unique_solved_count,
        'total_problems_count': total_problems_count,
        'coding_pct': int((unique_solved_count / max(total_problems_count, 1)) * 100),
        'easy_solved': easy_solved,
        'medium_solved': medium_solved,
        'hard_solved': hard_solved,
        'lang_breakdown': lang_breakdown,
        # Aptitude
        'total_quizzes': total_quizzes,
        'avg_accuracy': avg_accuracy,
        'accuracy_history_json': json.dumps(accuracy_history),
        # Interviews
        'interview_sessions': interview_sessions[:5],
        'avg_interview_score': avg_interview_score,
        # Activity Feed
        'activity_log': activity_log
    }
    return render(request, "progress.html", context)


@login_required
@require_POST
def set_daily_goal(request):
    """Feature 2: API to adjust student's daily learning targets"""
    try:
        data = json.loads(request.body)
        target_coding = max(1, int(data.get('target_coding', 2)))
        target_aptitude = max(1, int(data.get('target_aptitude', 5)))
        target_topics = max(1, int(data.get('target_topics', 1)))
        target_interviews = max(0, int(data.get('target_interviews', 1)))

        today = timezone.now().date()
        goal, _ = DailyGoal.objects.get_or_create(user=request.user, date=today)
        goal.target_coding = target_coding
        goal.target_aptitude = target_aptitude
        goal.target_topics = target_topics
        goal.target_interviews = target_interviews
        goal.save()

        stats = goal.completion_stats()
        return JsonResponse({'success': True, 'stats': stats, 'message': 'Daily goals updated successfully!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def _generate_personalized_recommendations(profile, solved_count=0, avg_accuracy=0):
    """Feature 6: Personalized Career Recommendation Engine analyzing profile, skills, and portal activity"""
    skills_text = (profile.skills or '').lower()
    interests_text = (profile.interests or '').lower()
    dept_text = (profile.department or '').lower()

    # Pre-defined career tracks with matching criteria
    career_tracks = [
        {
            'id': 'fullstack',
            'title': 'Full Stack Web Developer',
            'badge': 'High Placement Demand',
            'match_keywords': ['python', 'javascript', 'html', 'css', 'react', 'web', 'django', 'sql'],
            'salary': '₹6.5 - 18.0 LPA',
            'required_skills': ['Python / JavaScript', 'React / Modern Frontend', 'RESTful APIs', 'SQL Database Design', 'Git & CI/CD'],
            'description': 'Architect end-to-end web applications powering modern enterprises, startups, and SaaS products.',
            'recommended_tech': ['Python (Django/FastAPI)', 'React.js', 'PostgreSQL', 'Docker'],
            'projects': [
                'Full-Stack E-Commerce Portal with Razorpay Checkout',
                'Real-Time Collaborative Code Editor with WebSockets',
                'AI-Powered Job Application Tracker with Resume Analyzer'
            ],
            'action_plan': [
                'Solve 15 Full-Stack and JavaScript challenges in CareerVerse Coding Hub',
                'Master SQL Joins and Aggregations in the database section',
                'Build and deploy a complete portfolio project with REST APIs'
            ]
        },
        {
            'id': 'backend',
            'title': 'Backend & Cloud Systems Engineer',
            'badge': 'Core Engineering',
            'match_keywords': ['java', 'c++', 'go', 'python', 'sql', 'os', 'networking', 'backend'],
            'salary': '₹8.0 - 24.0 LPA',
            'required_skills': ['Java / Go / Python', 'Microservices Architecture', 'Relational & NoSQL Databases', 'Caching (Redis)', 'Linux & Docker'],
            'description': 'Build high-throughput, low-latency distributed systems that handle millions of requests reliably.',
            'recommended_tech': ['Java Spring Boot / Go', 'PostgreSQL & Redis', 'Docker & Kubernetes', 'Kafka / RabbitMQ'],
            'projects': [
                'Distributed URL Shortener with Sharded Redis Caching',
                'High-Concurrency Ticket Booking Engine with Optimistic Locking',
                'Microservices-based Authentication Service with JWT & OAuth2'
            ],
            'action_plan': [
                'Deep dive into DSA (Trees, Graphs, DP) in CareerVerse Workbench',
                'Revise OS (Processes, Threads, Deadlocks) and DBMS ACID properties',
                'Practice system design mock interviews on CareerVerse'
            ]
        },
        {
            'id': 'aiml',
            'title': 'AI & Machine Learning Engineer',
            'badge': 'Cutting-Edge Frontier',
            'match_keywords': ['ai', 'machine learning', 'data', 'python', 'numpy', 'pandas', 'deep learning'],
            'salary': '₹9.0 - 28.0 LPA',
            'required_skills': ['Python Data Stack (NumPy, Pandas)', 'Scikit-Learn & PyTorch', 'Linear Algebra & Statistics', 'LLM Prompt Engineering', 'Model Deployment'],
            'description': 'Develop, fine-tune, and deploy predictive models, computer vision systems, and generative AI agents.',
            'recommended_tech': ['Python', 'PyTorch / TensorFlow', 'HuggingFace & LangChain', 'FastAPI'],
            'projects': [
                'Automated Medical Document Summarizer with Open-Source LLMs',
                'Real-Time Fraud Detection Engine with Scikit-learn',
                'Visual Object Tracking & Recognition Pipeline with OpenCV'
            ],
            'action_plan': [
                'Complete all Python topics and coding challenges in CareerVerse',
                'Master Quantitative Aptitude and Probability in Aptitude Hub',
                'Experiment with LLM APIs and prompt engineering in the AI sandbox'
            ]
        },
        {
            'id': 'devops',
            'title': 'Cloud & DevOps Solutions Architect',
            'badge': 'Infrastructure Leader',
            'match_keywords': ['cloud', 'linux', 'aws', 'docker', 'devops', 'networking', 'security'],
            'salary': '₹7.5 - 20.0 LPA',
            'required_skills': ['Linux Shell Scripting', 'Docker & Containerization', 'Kubernetes Orchestration', 'AWS / Azure Cloud Services', 'Terraform (IaC)'],
            'description': 'Automate infrastructure deployment, orchestrate cloud containers, and ensure 99.99% system uptime.',
            'recommended_tech': ['Linux / Bash', 'Docker & Kubernetes', 'AWS / GCP', 'GitHub Actions / Jenkins'],
            'projects': [
                'Automated Multi-Stage CI/CD Deployment Pipeline with Docker',
                'High-Availability Kubernetes Cluster with Auto-Scaling',
                'Infrastructure-as-Code Setup for Cloud Web Services with Terraform'
            ],
            'action_plan': [
                'Study Linux commands and Operating Systems in CareerVerse CS Hub',
                'Learn Computer Networks fundamentals (TCP/IP, DNS, HTTP/HTTPS)',
                'Practice technical interview scenarios covering cloud availability'
            ]
        }
    ]

    # Calculate match percentage for each track
    analyzed_tracks = []
    for track in career_tracks:
        matches = 0
        total_kw = len(track['match_keywords'])
        for kw in track['match_keywords']:
            if kw in skills_text or kw in interests_text or kw in dept_text:
                matches += 1

        # Base score from keyword matching
        base_match = int((matches / total_kw) * 60) + 25

        # Boost from student portal performance
        if solved_count > 5:
            base_match += 8
        if avg_accuracy > 65:
            base_match += 7

        final_match = min(max(base_match, 45), 98)

        # Identify missing skills (Skill Gap)
        missing_skills = []
        for sk in track['required_skills']:
            first_word = sk.split()[0].lower().replace('/', ' ')
            if not any(w in skills_text for w in first_word.split()):
                missing_skills.append(sk)

        analyzed_tracks.append({
            **track,
            'match_percentage': final_match,
            'skill_gap': missing_skills[:3] or ['Advanced System Scalability', 'Production Deployment']
        })

    # Sort by match percentage descending
    analyzed_tracks.sort(key=lambda x: x['match_percentage'], reverse=True)
    return analyzed_tracks


# ==============================================================================
# CS LEARNING HUB VIEWS
# ==============================================================================

def cs_hub(request):
    """CS Learning Hub – main landing page showing all subjects."""
    subjects = Subject.objects.filter(is_active=True).order_by('order')

    # Annotate with user progress
    subjects_with_progress = []
    for subj in subjects:
        progress = 0
        if request.user.is_authenticated:
            progress = subj.get_progress_for_user(request.user)
        total_topics = subj.topics.filter(is_active=True).count()
        subjects_with_progress.append({
            'subject': subj,
            'progress': progress,
            'total_topics': total_topics,
        })

    # Group by category
    programming_langs = [s for s in subjects_with_progress if s['subject'].code in [
        'python', 'java', 'c', 'cpp', 'javascript', 'typescript', 'csharp', 'go', 'php', 'ruby', 'kotlin', 'swift', 'dart', 'sql'
    ]]
    cs_core = [s for s in subjects_with_progress if s['subject'].code in [
        'dsa', 'dbms', 'os', 'cn', 'oop', 'se', 'sysdesign'
    ]]
    advanced = [s for s in subjects_with_progress if s['subject'].code in [
        'ai', 'ml', 'cloud', 'linux', 'webdev', 'ds'
    ]]

    # Count total progress for logged-in user
    total_completed = 0
    total_topics_all = Topic.objects.filter(is_active=True).count()
    if request.user.is_authenticated:
        total_completed = StudentLearningProgress.objects.filter(
            user=request.user, is_completed=True
        ).count()

    return render(request, 'cs_hub.html', {
        'subjects': subjects_with_progress,
        'programming_langs': programming_langs,
        'cs_core': cs_core,
        'advanced': advanced,
        'total_completed': total_completed,
        'total_topics_all': total_topics_all,
    })


def subject_detail(request, subject_code):
    """View all topics for a specific subject."""
    subject = get_object_or_404(Subject, code=subject_code, is_active=True)
    topics = subject.topics.filter(is_active=True).order_by('order')

    # Annotate topics with user progress
    topics_with_status = []
    completed_ids = set()
    bookmarked_ids = set()
    if request.user.is_authenticated:
        progress_qs = StudentLearningProgress.objects.filter(
            user=request.user, topic__subject=subject
        )
        completed_ids = set(p.topic_id for p in progress_qs if p.is_completed)
        bookmarked_ids = set(p.topic_id for p in progress_qs if p.is_bookmarked)

    for topic in topics:
        topics_with_status.append({
            'topic': topic,
            'is_completed': topic.id in completed_ids,
            'is_bookmarked': topic.id in bookmarked_ids,
        })

    # Next topic to study
    next_topic = None
    for t in topics_with_status:
        if not t['is_completed']:
            next_topic = t['topic']
            break

    total = topics.count()
    completed_count = len(completed_ids)
    progress_pct = int((completed_count / total) * 100) if total > 0 else 0

    # Get related subjects
    all_subjects = Subject.objects.filter(is_active=True).exclude(code=subject_code)[:6]

    return render(request, 'subject_detail.html', {
        'subject': subject,
        'topics': topics_with_status,
        'next_topic': next_topic,
        'total_topics': total,
        'completed_count': completed_count,
        'progress_pct': progress_pct,
        'related_subjects': all_subjects,
    })


def topic_detail(request, topic_slug):
    """Individual lesson/topic page with content, code example and quiz."""
    topic = get_object_or_404(Topic, slug=topic_slug, is_active=True)
    subject = topic.subject

    # Get ordered topics for navigation
    all_topics = list(subject.topics.filter(is_active=True).order_by('order'))
    topic_ids = [t.id for t in all_topics]
    curr_idx = topic_ids.index(topic.id) if topic.id in topic_ids else 0
    prev_topic = all_topics[curr_idx - 1] if curr_idx > 0 else None
    next_topic = all_topics[curr_idx + 1] if curr_idx < len(all_topics) - 1 else None

    # User progress
    user_progress = None
    is_completed = False
    is_bookmarked = False
    quiz_score = None

    if request.user.is_authenticated:
        user_progress, _ = StudentLearningProgress.objects.get_or_create(
            user=request.user,
            topic=topic
        )
        is_completed = user_progress.is_completed
        is_bookmarked = user_progress.is_bookmarked
        quiz_score = user_progress.quiz_score

    # Mark as started (if not already tracked)
    if request.user.is_authenticated and user_progress and not user_progress.is_completed:
        pass  # viewed; they can mark complete

    # Get quiz questions
    quiz_questions = list(topic.quiz_questions.order_by('order')[:5])

    # Handle POST: mark complete or toggle bookmark
    if request.method == 'POST' and request.user.is_authenticated:
        action = request.POST.get('action', '')
        if action == 'mark_complete':
            user_progress.is_completed = True
            user_progress.completed_at = timezone.now()
            user_progress.save()
            messages.success(request, f"'{topic.title}' marked as completed!")
            return redirect('topic_detail', topic_slug=topic_slug)
        elif action == 'toggle_bookmark':
            user_progress.is_bookmarked = not user_progress.is_bookmarked
            user_progress.save()
            status = "bookmarked" if user_progress.is_bookmarked else "removed from bookmarks"
            messages.success(request, f"'{topic.title}' {status}.")
            return redirect('topic_detail', topic_slug=topic_slug)
        elif action == 'submit_quiz':
            # Score the quiz
            score = 0
            total_q = len(quiz_questions)
            for q in quiz_questions:
                selected = request.POST.get(f'quiz_{q.id}', '').upper()
                if selected == q.correct_option.upper():
                    score += 1
            user_progress.quiz_score = score
            user_progress.quiz_total = total_q
            if score >= total_q * 0.6:  # 60% to pass
                user_progress.is_completed = True
                user_progress.completed_at = timezone.now()
            user_progress.save()
            messages.success(request, f"Quiz scored: {score}/{total_q}!")
            return redirect('topic_detail', topic_slug=topic_slug)

    return render(request, 'topic_detail.html', {
        'topic': topic,
        'subject': subject,
        'prev_topic': prev_topic,
        'next_topic': next_topic,
        'is_completed': is_completed,
        'is_bookmarked': is_bookmarked,
        'quiz_score': quiz_score,
        'quiz_questions': quiz_questions,
        'curr_position': curr_idx + 1,
        'total_in_subject': len(all_topics),
    })


def learning_paths(request):
    """Display all available learning paths."""
    paths = LearningPath.objects.filter(is_active=True).order_by('order')

    paths_with_progress = []
    for path in paths:
        enrollment = None
        progress_pct = 0
        is_enrolled = False
        if request.user.is_authenticated:
            enrollment = StudentPathEnrollment.objects.filter(
                user=request.user, path=path
            ).first()
            if enrollment:
                is_enrolled = True
                progress_pct = enrollment.completion_percentage()

        total_steps = path.steps.count()
        paths_with_progress.append({
            'path': path,
            'is_enrolled': is_enrolled,
            'progress_pct': progress_pct,
            'enrollment': enrollment,
            'total_steps': total_steps,
        })

    return render(request, 'learning_paths.html', {
        'paths': paths_with_progress,
    })


def path_detail(request, path_code):
    """Detail view for a specific learning path, with enrollment."""
    path = get_object_or_404(LearningPath, code=path_code, is_active=True)
    steps = path.steps.order_by('step_number')

    enrollment = None
    is_enrolled = False
    progress_pct = 0
    if request.user.is_authenticated:
        enrollment = StudentPathEnrollment.objects.filter(
            user=request.user, path=path
        ).first()
        if enrollment:
            is_enrolled = True
            progress_pct = enrollment.completion_percentage()

    if request.method == 'POST' and request.user.is_authenticated:
        action = request.POST.get('action', '')
        if action == 'enroll':
            enrollment, created = StudentPathEnrollment.objects.get_or_create(
                user=request.user,
                path=path,
                defaults={'current_step': 1}
            )
            if created:
                messages.success(request, f"You're now enrolled in '{path.name}'!")
            else:
                messages.info(request, f"Already enrolled in '{path.name}'.")
            return redirect('path_detail', path_code=path_code)
        elif action == 'advance_step':
            if enrollment:
                total = steps.count()
                if enrollment.current_step < total:
                    enrollment.current_step += 1
                    enrollment.save()
            return redirect('path_detail', path_code=path_code)

    return render(request, 'path_detail.html', {
        'path': path,
        'steps': steps,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'progress_pct': progress_pct,
    })


def my_learning(request):
    """Student's personal learning dashboard – progress, enrollments, bookmarks."""
    if not request.user.is_authenticated:
        return redirect('login')

    # Enrolled paths
    enrollments = StudentPathEnrollment.objects.filter(
        user=request.user, is_active=True
    ).select_related('path').order_by('-enrolled_at')

    # Completed topics
    completed_progress = StudentLearningProgress.objects.filter(
        user=request.user, is_completed=True
    ).select_related('topic__subject').order_by('-completed_at')

    # Bookmarked topics
    bookmarks = StudentLearningProgress.objects.filter(
        user=request.user, is_bookmarked=True
    ).select_related('topic__subject')

    # Subject-wise breakdown
    subjects = Subject.objects.filter(is_active=True)
    subject_progress = []
    for subj in subjects:
        total = subj.topics.filter(is_active=True).count()
        if total == 0:
            continue
        done = completed_progress.filter(topic__subject=subj).count()
        if done > 0:
            subject_progress.append({
                'subject': subj,
                'completed': done,
                'total': total,
                'pct': int((done / total) * 100)
            })

    # Recently studied (last 5)
    recent = StudentLearningProgress.objects.filter(
        user=request.user
    ).select_related('topic__subject').order_by('-started_at')[:5]

    total_completed = completed_progress.count()
    total_topics = Topic.objects.filter(is_active=True).count()

    return render(request, 'my_learning.html', {
        'enrollments': enrollments,
        'completed_progress': completed_progress[:10],
        'bookmarks': bookmarks[:10],
        'subject_progress': subject_progress,
        'recent': recent,
        'total_completed': total_completed,
        'total_topics': total_topics,
        'overall_pct': int((total_completed / total_topics) * 100) if total_topics > 0 else 0,
    })


@require_POST
def mark_topic_progress(request):
    """AJAX: Toggle topic completion status."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
    try:
        data = json.loads(request.body)
        topic_id = data.get('topic_id')
        action = data.get('action', 'complete')

        topic = get_object_or_404(Topic, id=topic_id)
        progress, _ = StudentLearningProgress.objects.get_or_create(
            user=request.user, topic=topic
        )

        if action == 'complete':
            progress.is_completed = True
            progress.completed_at = timezone.now()
        elif action == 'uncomplete':
            progress.is_completed = False
            progress.completed_at = None
        elif action == 'bookmark':
            progress.is_bookmarked = not progress.is_bookmarked

        progress.save()
        return JsonResponse({
            'success': True,
            'is_completed': progress.is_completed,
            'is_bookmarked': progress.is_bookmarked
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def learn_search(request):
    """Global search across all learning materials."""
    query = request.GET.get('q', '').strip()
    subject_filter = request.GET.get('subject', 'all')
    difficulty_filter = request.GET.get('difficulty', 'all')

    topics = Topic.objects.filter(is_active=True)

    if query:
        topics = topics.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(content__icontains=query)
        )
    if subject_filter != 'all':
        topics = topics.filter(subject__code=subject_filter)
    if difficulty_filter != 'all':
        topics = topics.filter(difficulty=difficulty_filter)

    topics = topics.select_related('subject')[:40]

    # Also search coding problems
    coding_problems = []
    if query:
        coding_problems = CodingProblem.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )[:10]

    subjects = Subject.objects.filter(is_active=True)
    difficulties = ['Beginner', 'Easy', 'Medium', 'Hard', 'Expert']

    return render(request, 'learn_search.html', {
        'query': query,
        'topics': topics,
        'coding_problems': coding_problems,
        'subjects': subjects,
        'difficulties': difficulties,
        'selected_subject': subject_filter,
        'selected_difficulty': difficulty_filter,
        'total_results': topics.count(),
    })


# ==============================================================================
# REGISTER/LOGIN: AUTO-CREATE MEMBERSHIP
# ==============================================================================

def _ensure_membership(user):
    """Create StudentMembership with 50 free credits for new user."""
    StudentMembership.objects.get_or_create(
        user=user,
        defaults={'plan': 'free', 'ai_credits': 50}
    )
