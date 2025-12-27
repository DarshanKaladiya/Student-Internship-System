from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('FACULTY', 'Faculty'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    # FIXED: Added profile_pic to resolve FieldError
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png', blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    roll_no = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    semester = models.CharField(max_length=10, blank=True)
    skills = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Internship(models.Model):
    # Non-nullable faculty field requires a default during migration
    faculty = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
    )

    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    stipend = models.CharField(max_length=100, blank=True)
    required_skills = models.TextField(blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def days_left(self):
        """Calculates days remaining until the node expires."""
        if self.deadline:
            delta = self.deadline - timezone.now()
            return max(0, delta.days)
        return None

    def __str__(self):
        return self.title

class Application(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.student.username} - {self.internship.title}"