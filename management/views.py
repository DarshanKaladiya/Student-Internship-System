from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q

from .models import UserProfile, Internship, Application
from .forms import InternshipPostForm


# ---------------- HOME & AUTH ----------------

def home_landing(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            return redirect('faculty_dashboard' if profile.role == 'FACULTY' else 'student_dashboard')
        except UserProfile.DoesNotExist:
            pass
    return render(request, 'management/home.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('home_landing')
        messages.error(request, "Invalid credentials")
    return render(request, 'management/login.html')

def logout_user(request):
    logout(request)
    return redirect('home_landing')


# ---------------- REGISTRATION ----------------

def student_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'STUDENT'})
            return redirect('login')
    return render(request, 'management/register.html', {'form': UserCreationForm()})

def faculty_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = 'FACULTY'
            profile.save()
            return redirect('login')
    return render(request, 'management/faculty_register.html', {'form': UserCreationForm()})


# ---------------- PROFILE & DASHBOARD ----------------

@login_required
def student_edit_profile(request):
    """ Handles Resume File Uploads via request.FILES. """
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name')
        profile.academy_name = request.POST.get('academy_name')
        profile.major = request.POST.get('major')
        profile.gpa = request.POST.get('gpa')
        profile.skills = request.POST.get('skills')
        profile.bio = request.POST.get('bio')
        
        if request.FILES.get('resume'):
            profile.resume = request.FILES.get('resume')
            
        profile.save()
        messages.success(request, "Identity Hub updated.")
        return redirect('student_dashboard')
    return render(request, 'management/edit_profile.html', {'profile': profile})

@login_required
def student_dashboard(request):
    """ Displays Featured Nodes and Student Identity. """
    profile = get_object_or_404(UserProfile, user=request.user)
    applications = Application.objects.filter(student=request.user)
    featured_nodes = Internship.objects.all().order_by('-id')[:3]
    return render(request, 'management/student_dashboard.html', {
        'applications': applications, 'total_apps': applications.count(),
        'featured_nodes': featured_nodes, 'profile': profile
    })

@login_required
def faculty_dashboard(request):
    internships = Internship.objects.filter(faculty=request.user)
    applications = Application.objects.filter(internship__faculty=request.user, status='PENDING')
    return render(request, 'management/faculty_dashboard.html', {
        'internships': internships, 'applications': applications,
        'total_nodes': internships.count(), 'pending_signals': applications.count()
    })

@login_required
def view_student_profile(request, pk):
    """ Faculty view to download student resumes. """
    profile = get_object_or_404(UserProfile, user__pk=pk)
    return render(request, 'management/view_profile.html', {'profile': profile})


# ---------------- INTERNSHIP MANAGEMENT ----------------

@login_required
def post_internship(request):
    """ Matches the post_internship name in urls.py. """
    if request.method == "POST":
        form = InternshipPostForm(request.POST)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.faculty = request.user
            internship.save()
            return redirect('faculty_dashboard')
    else:
        form = InternshipPostForm()
    return render(request, 'management/post_internship.html', {'form': form})

def internship_list(request):
    query = request.GET.get('q', '')
    internships = Internship.objects.filter(Q(title__icontains=query) | Q(required_skills__icontains=query)) if query else Internship.objects.all()
    return render(request, 'management/internship_list.html', {'internships': internships, 'query': query})

def internship_detail(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    return render(request, 'management/internship_detail.html', {'internship': internship})

@login_required
def apply_internship(request, pk):
    Application.objects.get_or_create(student=request.user, internship_id=pk)
    return redirect('application_success')

@login_required
def application_success(request):
    """ Professional confirmation screen. """
    return render(request, 'management/application_success.html')

@login_required
def approve_application(request, pk):
    app = get_object_or_404(Application, pk=pk, internship__faculty=request.user)
    app.status = 'APPROVED'; app.save()
    return redirect('faculty_dashboard')

@login_required
def reject_application(request, pk):
    app = get_object_or_404(Application, pk=pk, internship__faculty=request.user)
    app.status = 'REJECTED'; app.save()
    return redirect('faculty_dashboard')