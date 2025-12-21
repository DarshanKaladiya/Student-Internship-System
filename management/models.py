from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('FACULTY', 'Faculty'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    
    # FIXED: Added missing fields to stop AttributeErrors
    full_name = models.CharField(max_length=100, blank=True, null=True)
    roll_no = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    semester = models.IntegerField(blank=True, null=True)
    
    # Student skills
    skills = models.CharField(max_length=500, blank=True, help_text="Enter skills separated by commas")

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Internship(models.Model):
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.CharField(max_length=500, blank=True, help_text="Skills separated by commas")
    location = models.CharField(max_length=100)
    stipend = models.CharField(max_length=50, default="Unpaid")
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    status_choices = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True) # Used for sorting
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')