from django import forms
from .models import UserProfile, Internship

class ProfileUpdateForm(forms.ModelForm):
    """
    Form for students to update their academic details.
    Resolves the missing attribute errors for full_name and roll_no.
    """
    class Meta:
        model = UserProfile
        fields = ['full_name', 'roll_no', 'department', 'semester', 'skills']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Full Name'}),
            'roll_no': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 21BCE100'}),
            'department': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Computer Science'}),
            'semester': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Current Semester'}),
            'skills': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'e.g. Python, SQL, React', 'rows': 3}),
        }

class InternshipForm(forms.ModelForm):
    """
    Form for faculty to post new internships.
    """
    class Meta:
        model = Internship
        fields = ['title', 'company_name', 'description', 'required_skills', 'location', 'stipend']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Internship Title'}),
            'company_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Company Name'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Detailed Job Description', 'rows': 4}),
            'required_skills': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Python, Java, Excel'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Remote, Mumbai, NY'}),
            'stipend': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. ₹15,000/mo or Unpaid'}),
        }