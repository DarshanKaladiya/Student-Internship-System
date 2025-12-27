from django import forms
from .models import UserProfile, Internship

class ProfileUpdateForm(forms.ModelForm):
    """Form for student academic identity synchronization."""
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'full_name', 'roll_no', 'department', 'semester', 'skills']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g. Python, React, SQL...'}),
        }

class InternshipForm(forms.ModelForm):
    """Form for initializing internship nodes with deadline logic."""
    class Meta:
        model = Internship
        fields = ['title', 'company_name', 'location', 'stipend', 'deadline', 'required_skills', 'description']
        widgets = {
            # Native datetime-local picker for modern browsers
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'glass-input'}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'required_skills': forms.TextInput(attrs={'placeholder': 'e.g. Python, Java, Figma'}),
        }