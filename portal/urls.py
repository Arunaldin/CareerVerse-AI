from django.urls import path
from . import views

urlpatterns = [
    # Core Landing & Info
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Authentication & Profile
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),

    # Student Dashboard & Progress Tracking
    path('dashboard/', views.dashboard, name='dashboard'),
    path('progress/', views.student_progress, name='student_progress'),
    path('api/daily-goal/', views.set_daily_goal, name='set_daily_goal'),

    # AI Career Guidance
    path('career-guidance/', views.career_guidance, name='career_guidance'),

    # Resume Builder
    path('resume/', views.resume, name='resume'),

    # Aptitude & Quiz Preparation
    path('aptitude/', views.aptitude, name='aptitude'),
    path('quiz/', views.quiz, name='quiz'),
    path('result/', views.result, name='result'),

    # Coding Preparation & Interactive Workbench
    path('coding/', views.coding, name='coding'),
    path('coding/<int:problem_id>/', views.coding_detail, name='coding_detail'),
    path('coding/run/', views.run_code_api, name='run_code_api'),

    # Placement Preparation & Company Hub
    path('placement/', views.placement, name='placement'),
    path('placement/compare/', views.company_compare, name='company_compare'),
    path('placement/<slug:company_slug>/', views.company_detail, name='company_detail'),

    # AI Mock Interview Preparation & Performance Reports
    path('interview/', views.interview, name='interview'),
    path('interview/evaluate/', views.interview_evaluate, name='interview_evaluate'),
    path('interview/report/<int:session_id>/', views.interview_report, name='interview_report'),
    path('interview/history/', views.interview_history, name='interview_history'),
    path('technical/', views.technical, name='technical'),
    path('hr/', views.hr, name='hr'),
]
