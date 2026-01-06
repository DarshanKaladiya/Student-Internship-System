from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('FACULTY', 'Faculty'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # ✅ Student Academic & Profile Details
    full_name = models.CharField(max_length=255, blank=True, null=True)
    academy_name = models.CharField(max_length=255, blank=True, null=True, help_text="College or University Name")
    major = models.CharField(max_length=255, blank=True, null=True, help_text="e.g. Computer Science")
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    skills = models.TextField(blank=True, null=True, help_text="Enter skills separated by commas")
    bio = models.TextField(blank=True, null=True, help_text="A brief introduction")

    def __str__(self):
        return self.user.username


class Internship(models.Model):
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    stipend = models.CharField(max_length=100)
    deadline = models.DateField()
    required_skills = models.TextField()
    description = models.TextField()
    faculty = models.ForeignKey(User, on_delete=models.CASCADE)
    external_apply_link = models.URLField(blank=True, null=True)

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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.internship.title}"