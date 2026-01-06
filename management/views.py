from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile, Internship, Application
from .forms import InternshipPostForm


# ---------------- HOME ----------------

def home_landing(request):
    """
    Redirects users based on their role after authentication.
    """
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.role == 'FACULTY':
                return redirect('faculty_dashboard')
            return redirect('student_dashboard')
        except UserProfile.DoesNotExist:
            pass
    return render(request, 'management/home.html')


# ---------------- AUTH ----------------

def login_view(request):
    """
    Handles user login and redirects to the landing controller.
    """
    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('home_landing')
        messages.error(request, "Invalid username or password")
    return render(request, 'management/login.html')


def logout_user(request):
    """
    Logs out the user and returns to the home screen.
    """
    logout(request)
    return redirect('home_landing')


# ---------------- REGISTRATION ----------------

def student_register(request):
    """
    Registers a new student and creates their UserProfile.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'STUDENT'}
            )
            messages.success(request, "Student registered successfully.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'management/register.html', {'form': form})


def faculty_register(request):
    """
    Registers a new faculty member and assigns the FACULTY role.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = 'FACULTY'
            profile.save()
            messages.success(request, "Faculty registered successfully.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'management/faculty_register.html', {'form': form})


# ---------------- PROFILE MANAGEMENT ----------------

@login_required
def student_edit_profile(request):
    """
    Allows students to update their academic and bio details.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name')
        profile.academy_name = request.POST.get('academy_name')
        profile.major = request.POST.get('major')
        profile.gpa = request.POST.get('gpa')
        profile.skills = request.POST.get('skills')
        profile.bio = request.POST.get('bio')
        profile.save()
        messages.success(request, "Academic identity record saved.")
        return redirect('student_dashboard')
        
    return render(request, 'management/edit_profile.html', {'profile': profile})


@login_required
def view_student_profile(request, pk):
    """
    Allows Faculty to view a student's profile during application review.
    """
    student_user = get_object_or_404(User, pk=pk)
    profile = get_object_or_404(UserProfile, user=student_user)
    return render(request, 'management/view_profile.html', {'profile': profile})


# ---------------- INTERNSHIP MANAGEMENT ----------------

@login_required
def post_internship(request):
    """
    Allows faculty to deploy new internship nodes to the network.
    """
    profile = UserProfile.objects.get(user=request.user)

    if profile.role != 'FACULTY':
        messages.error(request, "Only faculty can post internships.")
        return redirect('student_dashboard')

    if request.method == "POST":
        form = InternshipPostForm(request.POST)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.faculty = request.user
            internship.save()
            messages.success(request, "Internship deployed successfully.")
            return redirect('faculty_dashboard')
    else:
        form = InternshipPostForm()

    return render(request, 'management/post_internship.html', {'form': form})


def internship_list(request):
    """
    Displays all active internship nodes available in the system.
    """
    internships = Internship.objects.all()
    return render(request, 'management/internship_list.html', {
        'internships': internships
    })


def internship_detail(request, pk):
    """
    Displays full details for a specific internship node.
    """
    internship = get_object_or_404(Internship, pk=pk)
    return render(request, 'management/internship_detail.html', {
        'internship': internship
    })


@login_required
def apply_internship(request, pk):
    """
    Creates a pending application signal for a student.
    """
    internship = get_object_or_404(Internship, pk=pk)
    Application.objects.get_or_create(
        student=request.user,
        internship=internship
    )
    messages.success(request, "Application submitted successfully.")
    return redirect('student_dashboard')


# ---------------- APPROVE / REJECT ----------------

@login_required
def approve_application(request, pk):
    """
    Approves a student's application signal.
    """
    application = get_object_or_404(
        Application,
        pk=pk,
        internship__faculty=request.user
    )
    application.status = 'APPROVED'
    application.save()
    messages.success(request, "Application approved.")
    return redirect('faculty_dashboard')


@login_required
def reject_application(request, pk):
    """
    Rejects a student's application signal.
    """
    application = get_object_or_404(
        Application,
        pk=pk,
        internship__faculty=request.user
    )
    application.status = 'REJECTED'
    application.save()
    messages.success(request, "Application rejected.")
    return redirect('faculty_dashboard')


# ---------------- DASHBOARDS ----------------

@login_required
def student_dashboard(request):
    """
    Displays the student's identity hub and application signals.
    """
    applications = Application.objects.filter(student=request.user)
    return render(request, 'management/student_dashboard.html', {
        'applications': applications,
        'total_apps': applications.count()
    })


@login_required
def faculty_dashboard(request):
    """
    Displays the faculty command board, nodes, and pending signals.
    """
    internships = Internship.objects.filter(faculty=request.user)
    applications = Application.objects.filter(
        internship__faculty=request.user,
        status='PENDING'
    ).select_related('student__userprofile')

    return render(request, 'management/faculty_dashboard.html', {
        'internships': internships,
        'applications': applications,
        'total_nodes': internships.count(),
        'pending_signals': applications.count(),
    })