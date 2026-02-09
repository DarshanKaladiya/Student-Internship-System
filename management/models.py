from django.db import models
from django.contrib.auth.models import User

# ---------------- USER PROFILE ----------------

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('FACULTY', 'Faculty'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    
    # Common Fields
    full_name = models.CharField(max_length=100, blank=True, null=True)
    academy_name = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    # Faculty Fields
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    office_location = models.CharField(max_length=100, blank=True, null=True)
    research_interest = models.CharField(max_length=255, blank=True, null=True)
    
    # Student Fields
    major = models.CharField(max_length=100, blank=True, null=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

# ---------------- INTERNSHIPS ----------------

class Internship(models.Model):
    faculty = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_internships')
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, default="Institutional Dept")
    stipend = models.CharField(max_length=100, blank=True, null=True)
    external_apply_link = models.URLField(blank=True, null=True)
    description = models.TextField()
    required_skills = models.TextField()
    location = models.CharField(max_length=100, default="Remote")
    deadline = models.DateTimeField() 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ---------------- APPLICATIONS ----------------

class Application(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='application_set')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)