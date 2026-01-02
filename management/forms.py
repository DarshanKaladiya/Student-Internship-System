from django import forms
from .models import Internship

class InternshipPostForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = [
            'title',
            'company_name',
            'location',
            'stipend',
            'deadline',
            'required_skills',
            'description',
        ]
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
