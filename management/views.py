from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Internship, Application, UserProfile
from .forms import InternshipForm, ProfileUpdateForm

# --- Systems Intelligence View ---
def home_landing(request):
    """Provides system stats for the glassmorphism landing page."""
    context = {
        'total_students': UserProfile.objects.filter(role='STUDENT').count(),
        'available_internships': Internship.objects.count(),
        'recent_internships': Internship.objects.all().order_by('-posted_date')[:3]
    }
    return render(request, 'management/home.html', context)

# --- Authentication Module ---
def student_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user, role='STUDENT')
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'management/register.html', {'form': form, 'role': 'Student'})

def faculty_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user, role='FACULTY')
            login(request, user)
            return redirect('faculty_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'management/register.html', {'form': form, 'role': 'Faculty'})

def login_view(request):
    target_role = request.GET.get('role', 'Student') 
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('faculty_dashboard' if user.userprofile.role == 'FACULTY' else 'student_dashboard')
    return render(request, 'management/login.html', {'form': AuthenticationForm(), 'role': target_role})

# --- Profile Management ---
@login_required
def student_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Identity node synchronized.")
            return redirect('student_dashboard')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'management/student_profile.html', {'form': form})

# --- Faculty Control Logic ---
@login_required
def faculty_dashboard(request):
    internships = Internship.objects.filter(faculty=request.user)
    pending_applications = Application.objects.filter(internship__faculty=request.user, status='PENDING')
    return render(request, 'management/faculty_dashboard.html', {
        'internships': internships, 
        'pending_applications': pending_applications
    })

@login_required
def post_internship(request):
    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            intern = form.save(commit=False)
            intern.faculty = request.user
            intern.save()
            return redirect('faculty_dashboard')
    return render(request, 'management/post_internship.html', {'form': InternshipForm()})

# FIXED: Added missing review_application view
@login_required
def review_application(request, pk, status):
    """Processes faculty decisions on student applications."""
    app = get_object_or_404(Application, pk=pk, internship__faculty=request.user)
    if status in ['APPROVED', 'REJECTED']:
        app.status = status
        app.save()
        messages.success(request, f"Application status updated to {status}.")
    return redirect('faculty_dashboard')

# --- Student & Marketplace Logic ---
def internship_list(request):
    internships = Internship.objects.all().order_by('-posted_date')
    return render(request, 'management/internship_list.html', {'internships': internships})

def internship_detail(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    return render(request, 'management/internship_detail.html', {'internship': internship})

@login_required
def student_dashboard(request):
    apps = Application.objects.filter(student=request.user)
    return render(request, 'management/student_dashboard.html', {'applications': apps})

@login_required
def apply_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    Application.objects.get_or_create(student=request.user, internship=internship)
    messages.success(request, "Signal transmitted.")
    return redirect('student_dashboard')

def logout_user(request):
    logout(request)
    return redirect('home')