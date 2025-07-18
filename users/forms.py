from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import UserProfile
from django import forms

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'full_name',
            'phone_number',
            'location',
            'skills',
            'education',
            'experience',
            'projects',
            'achievements',
            'resume_template_choice'
        ]
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 2}),
            'education': forms.Textarea(attrs={'rows': 2}),
            'experience': forms.Textarea(attrs={'rows': 2}),
            'projects': forms.Textarea(attrs={'rows': 2}),
            'achievements': forms.Textarea(attrs={'rows': 2}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
