from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Student, StudentProfile, SavedResume


class StudentForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a unique username',
            'required': 'required'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a secure password',
            'required': 'required'
        })
    )

    class Meta:
        model = Student
        fields = ['name', 'email', 'phone', 'username', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 9876543210'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose another.')
        return username


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'college',
            'department',
            'cgpa',
            'graduation_year',
            'skills',
            'interests',
            'profile_picture',
        ]
        widgets = {
            'college': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Stanford / IIT Madras'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Computer Science and Engineering'}),
            'cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '10', 'placeholder': '8.50'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2026'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, SQL, React, Data Structures, Django'}),
            'interests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g. Artificial Intelligence, Cloud Computing, Full-Stack Web Development'
            }),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class SavedResumeForm(forms.ModelForm):
    class Meta:
        model = SavedResume
        fields = ['title', 'template_name']
