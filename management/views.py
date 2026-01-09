from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q

from .models import UserProfile, Internship, Application
from .forms import InternshipPostForm


# ---------------- HOME / GATEKEEPER ----------------

def home_landing(request):
    """
    Landing page logic.
    GATEKEEPER: If user is authenticated, they are blocked from this page 
    and redirected to their dashboard.
    """
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.role == 'FACULTY':
                return redirect('faculty_dashboard')
            else:
                return redirect('student_dashboard')
        except UserProfile.DoesNotExist:
            # Fallback for superusers or users without profiles
            pass 

    # Content for Guest Users Only
    node_count = Internship.objects.count()
    user_count = User.objects.count()
    vetting_rate = "98%" 

    return render(request, 'management/home.html', {
        'node_count': node_count,
        'user_count': user_count,
        'vetting_rate': vetting_rate
    })


# ---------------- AUTHENTICATION ----------------

def login_view(request):
    """
    Handles secure entry and role-based redirection.
    """
    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username'), 
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            # Immediate role-based routing after successful login
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.role == 'FACULTY':
                    return redirect('faculty_dashboard')
                else:
                    return redirect('student_dashboard')
            except UserProfile.DoesNotExist:
                return redirect('home_landing')
        
        messages.error(request, "Invalid username or password")
    return render(request, 'management/login.html')


def logout_user(request):
    """
    Ends session and returns user to the public landing page.
    """
    logout(request)
    return redirect('home_landing')


# ---------------- REGISTRATION ----------------

def student_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'STUDENT'})
            messages.success(request, "Student Identity Node created. Please login.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'management/register.html', {'form': form})


def faculty_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = 'FACULTY'
            profile.save()
            messages.success(request, "Faculty Command Node created. Please login.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'management/faculty_register.html', {'form': form})


# ---------------- DASHBOARDS ----------------

@login_required
def faculty_dashboard(request):
    """
    Protected faculty command center.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    internships = Internship.objects.filter(faculty=request.user)
    applications = Application.objects.filter(
        internship__faculty=request.user, 
        status='PENDING'
    ).select_related('student__userprofile', 'internship')
    
    return render(request, 'management/faculty_dashboard.html', {
        'profile': profile,
        'internships': internships, 
        'applications': applications,
        'total_nodes': internships.count(), 
        'pending_signals': applications.count()
    })


@login_required
def student_dashboard(request):
    """
    Protected student identity hub.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    applications = Application.objects.filter(student=request.user)
    featured_nodes = Internship.objects.all().order_by('-id')[:3]
    return render(request, 'management/student_dashboard.html', {
        'applications': applications, 
        'total_apps': applications.count(),
        'featured_nodes': featured_nodes, 
        'profile': profile
    })


# ---------------- INTERNSHIP ACTIONS ----------------

@login_required
def internship_list(request):
    """
    Search engine for internships. Accessible via the Student Dashboard.
    """
    query = request.GET.get('q', '')
    if query:
        internships = Internship.objects.filter(
            Q(title__icontains=query) | 
            Q(required_skills__icontains=query)
        )
    else:
        internships = Internship.objects.all()
        
    return render(request, 'management/internship_list.html', {
        'internships': internships,
        'query': query
    })


@login_required
def internship_detail(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    return render(request, 'management/internship_detail.html', {'internship': internship})


@login_required
def post_internship(request):
    if request.method == "POST":
        form = InternshipPostForm(request.POST)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.faculty = request.user
            internship.save()
            return redirect('faculty_dashboard')
    return render(request, 'management/post_internship.html', {'form': InternshipPostForm()})


@login_required
def apply_internship(request, pk):
    Application.objects.get_or_create(student=request.user, internship_id=pk)
    return redirect('application_success')


@login_required
def application_success(request):
    return render(request, 'management/application_success.html')


@login_required
def approve_application(request, pk):
    app = get_object_or_404(Application, pk=pk, internship__faculty=request.user)
    app.status = 'APPROVED'
    app.save()
    return redirect('faculty_dashboard')


@login_required
def reject_application(request, pk):
    app = get_object_or_404(Application, pk=pk, internship__faculty=request.user)
    app.status = 'REJECTED'
    app.save()
    return redirect('faculty_dashboard')


@login_required
def view_student_profile(request, student_pk, internship_pk):
    student_profile = get_object_or_404(UserProfile, user__pk=student_pk)
    internship = get_object_or_404(Internship, pk=internship_pk)
    application = get_object_or_404(Application, student__pk=student_pk, internship__pk=internship_pk)
    
    return render(request, 'management/view_profile.html', {
        'profile': student_profile,
        'internship': internship,
        'application': application
    })


@login_required
def student_edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name')
        profile.academy_name = request.POST.get('academy_name')
        profile.major = request.POST.get('major')
        profile.gpa = request.POST.get('gpa')
        profile.skills = request.POST.get('skills')
        if request.FILES.get('resume'):
            profile.resume = request.FILES.get('resume')
        profile.save()
        return redirect('student_dashboard')
    return render(request, 'management/edit_profile.html', {'profile': profile})