from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Internship, Application, UserProfile
from .forms import InternshipForm, ProfileUpdateForm

# --- Systems Intelligence (Home) ---
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
    """Handles student account creation and role assignment."""
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
    """Handles faculty account creation and role assignment."""
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
    """Role-based login with portal validation."""
    target_role = request.GET.get('role', 'Student') 
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            user_role = user.userprofile.role
            if target_role == "Student" and user_role != "STUDENT":
                messages.error(request, "⚠️ Use Faculty Portal for this account.")
            elif target_role == "Faculty" and user_role != "FACULTY":
                messages.error(request, "⚠️ Use Student Portal for this account.")
            else:
                login(request, user)
                return redirect('faculty_dashboard' if user_role == 'FACULTY' else 'student_dashboard')
    return render(request, 'management/login.html', {'form': AuthenticationForm(), 'role': target_role})

# --- Profile Management ---
@login_required
def student_profile(request):
    """FIXED: Uses get_or_create to prevent RelatedObjectDoesNotExist."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'management/student_profile.html', {'form': form})

# --- Faculty Control Logic ---
@login_required
def faculty_dashboard(request):
    """Faculty view of active nodes and pending student signals."""
    if request.user.userprofile.role != 'FACULTY':
        return redirect('student_dashboard')
    internships = Internship.objects.filter(faculty=request.user)
    pending_apps = Application.objects.filter(internship__faculty=request.user, status='PENDING')
    return render(request, 'management/faculty_dashboard.html', {
        'internships': internships, 
        'pending_applications': pending_apps
    })

@login_required
def post_internship(request):
    """Initializes new internship nodes linked to the posting faculty."""
    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            intern = form.save(commit=False)
            intern.faculty = request.user
            intern.save()
            messages.success(request, "Node broadcasted successfully.")
            return redirect('faculty_dashboard')
    return render(request, 'management/post_internship.html', {'form': InternshipForm()})

@login_required
def review_application(request, pk, status):
    """Processes faculty decisions on student applications."""
    app = get_object_or_404(Application, pk=pk, internship__faculty=request.user)
    if status in ['APPROVED', 'REJECTED']:
        app.status = status
        app.save()
    return redirect('faculty_dashboard')

# --- Student Marketplace & Dashboard ---
def internship_list(request):
    """Marketplace with real-time search filtering."""
    query = request.GET.get('search', '')
    if query:
        internships = Internship.objects.filter(
            Q(title__icontains=query) | Q(company_name__icontains=query)
        ).order_by('-posted_date')
    else:
        internships = Internship.objects.all().order_by('-posted_date')
    return render(request, 'management/internship_list.html', {'internships': internships, 'query': query})

def internship_detail(request, pk):
    """Detailed intelligence view for specific nodes."""
    internship = get_object_or_404(Internship, pk=pk)
    return render(request, 'management/internship_detail.html', {'internship': internship})

@login_required
def apply_internship(request, pk):
    """Transmits application signal to faculty leads."""
    internship = get_object_or_404(Internship, pk=pk)
    if request.user.userprofile.role == 'STUDENT':
        Application.objects.get_or_create(student=request.user, internship=internship)
        messages.success(request, "Signal transmitted to faculty.")
    return redirect('student_dashboard')

@login_required
def student_dashboard(request):
    apps = Application.objects.filter(student=request.user)
    return render(request, 'management/student_dashboard.html', {'applications': apps})

def logout_user(request):
    logout(request)
    return redirect('home')