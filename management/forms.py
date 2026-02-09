from django import forms
from .models import Internship

class InternshipPostForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = [
            'title', 
            'company_name', 
            'stipend', 
            'location', 
            'deadline', 
            'required_skills', 
            'description', 
            'external_apply_link'
        ]
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'sync-input'}),
        }