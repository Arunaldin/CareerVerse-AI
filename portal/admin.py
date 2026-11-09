from django.contrib import admin
from .models import (
    Student, StudentProfile, AptitudeQuestion, QuizAttempt,
    CodingProblem, CodingSubmission, CompanyPlacement,
    SavedResume, CareerGuidanceResult, InterviewPracticeSession,
    FoundingMemberOffer, StudentMembership
)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'college', 'department', 'cgpa', 'graduation_year')
    search_fields = ('user__username', 'college', 'department')

@admin.register(CodingProblem)
class CodingProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'slug')
    list_filter = ('category', 'difficulty')
    search_fields = ('title', 'description')

@admin.register(CodingSubmission)
class CodingSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'status', 'passed_count', 'total_tests', 'created_at')
    list_filter = ('status', 'created_at')

@admin.register(AptitudeQuestion)
class AptitudeQuestionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'category', 'difficulty', 'correct_option')
    list_filter = ('category', 'difficulty')
    search_fields = ('question_text', 'topic')

@admin.register(CompanyPlacement)
class CompanyPlacementAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'package_range', 'eligibility_cgpa')
    list_filter = ('category',)
    search_fields = ('name', 'overview')

@admin.register(StudentMembership)
class StudentMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'ai_credits', 'is_founding_member', 'created_at')
    list_filter = ('plan', 'is_founding_member')

@admin.register(FoundingMemberOffer)
class FoundingMemberOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'max_slots', 'is_active', 'created_at')
