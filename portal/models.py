from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ==============================================================================
# FOUNDING 100 & SUBSCRIPTION MANAGEMENT
# ==============================================================================

class FoundingMemberOffer(models.Model):
    title = models.CharField(max_length=100, default='CareerVerse Founding 100 – FREE')
    max_slots = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)
    description = models.TextField(default='Free early-access membership for the first 100 verified students with all premium preparation modules included.')
    created_at = models.DateTimeField(auto_now_add=True)

    def remaining_slots(self):
        claimed = StudentMembership.objects.filter(is_founding_member=True).count()
        return max(0, self.max_slots - claimed)

    def __str__(self):
        return f"{self.title} ({self.remaining_slots()} slots left)"


class StudentMembership(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free Student Tier (₹0)'),
        ('founding', 'Founding 100 Early Access (₹0)'),
        ('launch_offer', 'Launch Special (₹9)'),
        ('monthly_premium', 'Monthly Premium (₹49/mo)'),
        ('yearly_premium', 'Yearly Pro Pass (₹399/yr)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='membership')
    plan = models.CharField(max_length=30, choices=PLAN_CHOICES, default='free')
    is_founding_member = models.BooleanField(default=False)
    founding_seat_number = models.IntegerField(null=True, blank=True)
    ai_credits = models.IntegerField(default=50, help_text="AI Credits for tutor & roadmap queries")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_plan_display()} (Credits: {self.ai_credits})"


# Existing Student model (Preserved for compatibility)
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


# Existing Student Profile model (Preserved for compatibility)
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='studentprofile')
    college = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2)
    graduation_year = models.IntegerField()
    skills = models.TextField()

    interests = models.TextField(
        blank=True,
        help_text="Enter your interests, e.g. AI, Web Development, Data Science"
    )

    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    # Learning Streak System
    current_streak = models.IntegerField(default=1)
    longest_streak = models.IntegerField(default=1)
    last_active_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def update_streak(self):
        """Updates the learning streak when a student performs a learning action today."""
        today = timezone.now().date()
        if self.last_active_date == today:
            return self.current_streak

        from datetime import timedelta
        if self.last_active_date == today - timedelta(days=1):
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
        elif self.last_active_date is None or self.last_active_date < today - timedelta(days=1):
            self.current_streak = 1

        self.last_active_date = today
        self.save(update_fields=['current_streak', 'longest_streak', 'last_active_date'])
        return self.current_streak

    def completion_percentage(self):
        """Calculate profile completion percentage"""
        fields = [
            self.college, self.department, self.cgpa,
            self.graduation_year, self.skills, self.interests, self.profile_picture
        ]
        filled = sum(1 for f in fields if f)
        total = len(fields) + 2
        filled += 1
        if self.user.email:
            filled += 1
        return int((filled / total) * 100)


# ==============================================================================
# DAILY LEARNING GOALS
# ==============================================================================

class DailyGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_goals')
    date = models.DateField(default=timezone.now)
    target_coding = models.IntegerField(default=2)
    target_aptitude = models.IntegerField(default=5)
    target_topics = models.IntegerField(default=1)
    target_interviews = models.IntegerField(default=1)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'date']

    def __str__(self):
        return f"Daily Goals for {self.user.username} on {self.date}"

    def get_actual_coding(self):
        return CodingSubmission.objects.filter(
            user=self.user,
            created_at__date=self.date,
            status='Passed'
        ).values('problem').distinct().count()

    def get_actual_aptitude(self):
        attempts = QuizAttempt.objects.filter(user=self.user, created_at__date=self.date)
        return sum(a.total_questions for a in attempts)

    def get_actual_topics(self):
        return StudentLearningProgress.objects.filter(
            user=self.user,
            completed_at__date=self.date,
            is_completed=True
        ).count()

    def get_actual_interviews(self):
        return InterviewPracticeSession.objects.filter(
            user=self.user,
            created_at__date=self.date
        ).count()

    def completion_stats(self):
        actual_code = self.get_actual_coding()
        actual_apt = self.get_actual_aptitude()
        actual_top = self.get_actual_topics()
        actual_int = self.get_actual_interviews()

        parts = [
            min(actual_code / max(self.target_coding, 1), 1.0),
            min(actual_apt / max(self.target_aptitude, 1), 1.0),
            min(actual_top / max(self.target_topics, 1), 1.0),
            min(actual_int / max(self.target_interviews, 1), 1.0),
        ]
        pct = int((sum(parts) / len(parts)) * 100)
        return {
            'coding': {'actual': actual_code, 'target': self.target_coding, 'done': actual_code >= self.target_coding},
            'aptitude': {'actual': actual_apt, 'target': self.target_aptitude, 'done': actual_apt >= self.target_aptitude},
            'topics': {'actual': actual_top, 'target': self.target_topics, 'done': actual_top >= self.target_topics},
            'interviews': {'actual': actual_int, 'target': self.target_interviews, 'done': actual_int >= self.target_interviews},
            'percent': pct,
            'is_all_done': pct >= 100
        }


# ==============================================================================
# APTITUDE PREPARATION MODELS
# ==============================================================================

class AptitudeQuestion(models.Model):
    CATEGORY_CHOICES = [
        ('quantitative', 'Quantitative Aptitude'),
        ('logical', 'Logical Reasoning'),
        ('verbal', 'Verbal Ability'),
    ]

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='quantitative')
    topic = models.CharField(max_length=100, help_text="e.g. Percentages, Syllogisms, Reading Comprehension")
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=2, help_text="A, B, C, or D")
    explanation = models.TextField(blank=True, help_text="Detailed step-by-step solution")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Medium')

    def __str__(self):
        return f"[{self.get_category_display()}] {self.topic}: {self.question_text[:50]}..."


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    category = models.CharField(max_length=50, default='All')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=10)
    accuracy = models.FloatField(default=0.0)
    time_taken_seconds = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category}: {self.score}/{self.total_questions}"


# ==============================================================================
# CODING PREPARATION MODELS
# ==============================================================================

class CodingProblem(models.Model):
    CATEGORY_CHOICES = [
        ('python', 'Programming'),
        ('sql', 'SQL Queries'),
        ('dsa', 'Data Structures & Algorithms'),
    ]

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='python')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Easy')
    description = models.TextField()
    constraints = models.TextField(blank=True)
    sample_input = models.TextField(blank=True)
    sample_output = models.TextField(blank=True)
    starter_code = models.TextField(default='# Write your code here\n')
    solution_code = models.TextField(blank=True)
    solution_hint = models.TextField(blank=True)
    test_cases = models.JSONField(default=list, blank=True, help_text="List of {input, expected_output}")

    # Detailed Explanations & Complexity Analysis
    explanation = models.TextField(blank=True, help_text="Step-by-step logic, intuition and explanation")
    time_complexity = models.CharField(max_length=50, default='O(N)', blank=True)
    space_complexity = models.CharField(max_length=50, default='O(1)', blank=True)
    solution_python = models.TextField(blank=True)
    solution_java = models.TextField(blank=True)
    solution_cpp = models.TextField(blank=True)
    solution_c = models.TextField(blank=True)

    def __str__(self):
        return f"[{self.difficulty}] {self.title}"


class CodingSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coding_submissions')
    problem = models.ForeignKey(CodingProblem, on_delete=models.CASCADE, related_name='submissions')
    language = models.CharField(max_length=30, default='python', blank=True)
    code = models.TextField()
    status = models.CharField(max_length=50, default='Passed')  # Passed, Failed, Syntax Error
    passed_count = models.IntegerField(default=0)
    total_tests = models.IntegerField(default=0)
    output_log = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} ({self.status})"


# ==============================================================================
# PLACEMENT PREPARATION (COMPANY-WISE) MODELS
# ==============================================================================

class CompanyPlacement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=50, default='IT Services')  # IT Services, Product, Tech Giant, Consulting
    logo_icon = models.CharField(max_length=50, default='briefcase')
    accent_color = models.CharField(max_length=20, default='#2563eb')
    package_range = models.CharField(max_length=100, default='3.6 - 9.0 LPA')
    eligibility_cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=6.00)
    eligible_branches = models.CharField(max_length=255, default='CSE, IT, ECE, EEE, Mech, Civil')
    backlogs_allowed = models.CharField(max_length=100, default='0 active backlogs')
    overview = models.TextField(blank=True)
    selection_rounds = models.JSONField(default=list, blank=True)  # [{name, desc, duration, questions}]
    previous_questions = models.JSONField(default=list, blank=True)  # [{question, type, answer}]
    interview_tips = models.TextField(blank=True)

    # Verified Criteria vs General Guidance
    is_verified_criteria = models.BooleanField(default=True, help_text="True if criteria comes from verified campus placement drives")
    verified_source = models.CharField(max_length=255, default='Official Campus Recruitment Drives & University Placement Records', blank=True)

    # Specific Preparation Syllabus & Questions
    aptitude_topics = models.JSONField(default=list, blank=True)  # List of string topics
    coding_topics = models.JSONField(default=list, blank=True)    # List of string topics
    technical_questions = models.JSONField(default=list, blank=True)  # [{question, topic, answer}]
    hr_questions = models.JSONField(default=list, blank=True)         # [{question, tip, model_answer}]
    roadmap = models.JSONField(default=list, blank=True)              # 4-week preparation milestones

    def __str__(self):
        return self.name


# ==============================================================================
# RESUME BUILDER MODELS
# ==============================================================================

class SavedResume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=150, default='My Professional Resume')
    template_name = models.CharField(max_length=50, default='modern')  # modern, executive, minimalist, creative
    resume_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Resume - {self.title}"


# ==============================================================================
# AI CAREER GUIDANCE & INTERVIEW HISTORY
# ==============================================================================

class CareerGuidanceResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='career_results')
    degree = models.CharField(max_length=150)
    cgpa = models.CharField(max_length=20)
    skills = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    ai_result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        uname = self.user.username if self.user else "Anonymous"
        return f"Career Guidance for {uname} on {self.created_at.strftime('%Y-%m-%d')}"


class InterviewPracticeSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='interview_sessions')
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    skills = models.TextField(blank=True)
    experience = models.CharField(max_length=100, default='Fresher')
    interview_type = models.CharField(max_length=50, default='Technical')
    ai_result = models.TextField()
    evaluations = models.JSONField(default=list, blank=True)

    # Detailed Interview Performance Report
    overall_score = models.IntegerField(default=75)
    technical_score = models.IntegerField(default=70)
    communication_score = models.IntegerField(default=80)
    confidence_score = models.IntegerField(default=75)
    strengths = models.JSONField(default=list, blank=True)
    weaknesses = models.JSONField(default=list, blank=True)
    improvement_suggestions = models.JSONField(default=list, blank=True)
    recommended_topics = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        uname = self.user.username if self.user else "Anonymous"
        return f"Interview ({self.role} @ {self.company}) for {uname}"


# ==============================================================================
# CS LEARNING HUB MODELS
# ==============================================================================

class Subject(models.Model):
    """Top-level CS subjects: Python, DSA, DBMS, OS, CN, OOP, etc."""
    SUBJECT_CHOICES = [
        ('python', 'Python Programming'),
        ('java', 'Java Programming'),
        ('c', 'C Programming'),
        ('cpp', 'C++ Programming'),
        ('javascript', 'JavaScript'),
        ('typescript', 'TypeScript'),
        ('csharp', 'C#'),
        ('go', 'Go'),
        ('php', 'PHP'),
        ('ruby', 'Ruby'),
        ('kotlin', 'Kotlin'),
        ('swift', 'Swift'),
        ('dart', 'Dart'),
        ('sql', 'SQL & Databases'),
        ('dsa', 'Data Structures & Algorithms'),
        ('dbms', 'Database Management Systems'),
        ('os', 'Operating Systems'),
        ('cn', 'Computer Networks'),
        ('oop', 'Object-Oriented Programming'),
        ('se', 'Software Engineering'),
        ('coa', 'Computer Organization & Architecture'),
        ('toc', 'Theory of Computation'),
        ('compiler', 'Compiler Design'),
        ('discrete', 'Discrete Mathematics'),
        ('cloud', 'Cloud Computing'),
        ('security', 'Cybersecurity'),
        ('webdev', 'Web Development'),
        ('ai', 'Artificial Intelligence'),
        ('ml', 'Machine Learning'),
        ('ds', 'Data Science'),
        ('sysdesign', 'System Design'),
        ('linux', 'Linux & Command Line'),
    ]

    code = models.CharField(max_length=20, unique=True, choices=SUBJECT_CHOICES)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='📚')
    accent_color = models.CharField(max_length=20, default='#8b5cf6')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    total_topics = models.IntegerField(default=0)
    difficulty_level = models.CharField(max_length=20, default='Beginner', choices=[
        ('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('All Levels', 'All Levels')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_progress_for_user(self, user):
        if not user.is_authenticated:
            return 0
        total = self.topics.count()
        if total == 0:
            return 0
        completed = StudentLearningProgress.objects.filter(
            user=user, topic__subject=self, is_completed=True
        ).count()
        return int((completed / total) * 100)


class Topic(models.Model):
    """Individual topics within a subject."""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField(blank=True)
    content = models.TextField(blank=True, help_text="Main lesson content in Markdown/HTML")
    code_example = models.TextField(blank=True)
    language = models.CharField(max_length=30, default='python', help_text="Code language for syntax highlighting")
    difficulty = models.CharField(max_length=20, choices=[
        ('Beginner', 'Beginner'), ('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard'), ('Expert', 'Expert')
    ], default='Beginner')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    estimated_minutes = models.IntegerField(default=15, help_text="Estimated reading and practice time in minutes")
    has_quiz = models.BooleanField(default=False)
    has_exercise = models.BooleanField(default=False)
    interview_questions = models.JSONField(default=list, blank=True, help_text="List of common interview Q&A for this topic")
    key_points = models.JSONField(default=list, blank=True, help_text="Key takeaways as a list of strings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['subject', 'order']

    def __str__(self):
        return f"[{self.subject.name}] {self.title}"


class TopicQuiz(models.Model):
    """Quiz questions for a topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='quiz_questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=2)
    explanation = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, default='Easy')
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"Q: {self.question_text[:60]}..."


class LearningPath(models.Model):
    """Structured learning paths like 'Placement Preparation', 'Python Developer' etc."""
    PATH_CHOICES = [
        ('beginner_to_dev', 'Complete Beginner to Software Developer'),
        ('python_dev', 'Python Developer'),
        ('java_dev', 'Java Developer'),
        ('cpp_dev', 'C/C++ Programmer'),
        ('fullstack_dev', 'Full Stack Developer'),
        ('data_analyst', 'Data Analyst'),
        ('ai_ml', 'AI/ML Beginner'),
        ('placement', 'Placement Preparation (Campus)'),
        ('custom', 'Custom Path'),
    ]

    code = models.CharField(max_length=50, unique=True, choices=PATH_CHOICES)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='🗺️')
    accent_color = models.CharField(max_length=20, default='#8b5cf6')
    target_role = models.CharField(max_length=100, blank=True)
    duration_weeks = models.IntegerField(default=12)
    difficulty_level = models.CharField(max_length=20, default='Beginner')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class LearningPathStep(models.Model):
    """Individual steps/milestones in a learning path."""
    path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='steps')
    step_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    topics_to_cover = models.JSONField(default=list, blank=True)
    estimated_days = models.IntegerField(default=7)
    is_milestone = models.BooleanField(default=False)
    resources = models.JSONField(default=list, blank=True, help_text="[{title, url, type}]")

    class Meta:
        ordering = ['path', 'step_number']

    def __str__(self):
        return f"[{self.path.name}] Step {self.step_number}: {self.title}"


class StudentLearningProgress(models.Model):
    """Tracks individual topic completion for each student."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_progress')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='student_progress')
    is_completed = models.BooleanField(default=False)
    is_bookmarked = models.BooleanField(default=False)
    quiz_score = models.IntegerField(null=True, blank=True)
    quiz_total = models.IntegerField(null=True, blank=True)
    time_spent_minutes = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'topic']

    def __str__(self):
        status = "✓" if self.is_completed else "○"
        return f"{status} {self.user.username} → {self.topic.title}"


class StudentPathEnrollment(models.Model):
    """Tracks which learning paths a student has enrolled in."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='path_enrollments')
    path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='enrollments')
    current_step = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    target_completion_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'path']

    def completion_percentage(self):
        total_steps = self.path.steps.count()
        if total_steps == 0:
            return 0
        return min(int(((self.current_step - 1) / total_steps) * 100), 100)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.path.name}"
