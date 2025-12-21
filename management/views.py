from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Application, Internship
from django.contrib import messages

def home_landing(request):
    # FIXED: Replaced 'created_at' with 'posted_date'
    internships = Internship.objects.all().order_by('-posted_date')[:4]
    return render(request, 'management/home.html', {'internships': internships})

def login_view(request):
    role = request.GET.get('role', 'Student')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if hasattr(user, 'userprofile') and user.userprofile.role == 'FACULTY':
                return redirect('faculty_dashboard')
            return redirect('student_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'management/login.html', {'form': form, 'role': role})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'STUDENT'})
            login(request, user)
            return redirect('student_dashboard')
    return render(request, 'management/register.html', {'form': UserCreationForm(), 'role': 'Student'})

def faculty_register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'FACULTY'})
            login(request, user)
            return redirect('faculty_dashboard')
    return render(request, 'management/register.html', {'form': UserCreationForm(), 'role': 'Faculty'})

@login_required
def faculty_dashboard(request):
    # FIXED: Querying specifically through the internship relation to avoid ValueError
    if request.user.userprofile.role != 'FACULTY':
        return redirect('home')
    apps = Application.objects.filter(internship__faculty=request.user)
    return render(request, 'management/faculty_dashboard.html', {'applications': apps})

# ADDED: This function resolves the AttributeError shown in your terminal
@login_required
def update_status(request, app_id, new_status):
    application = get_object_or_404(Application, id=app_id)
    application.status = new_status
    application.save()
    messages.success(request, f"Application marked as {new_status}")
    return redirect('faculty_dashboard')

@login_required
def student_dashboard(request):
    # Ensure you have student_dashboard.html in templates/management/
    apps = Application.objects.filter(student=request.user).order_by('-applied_on')
    return render(request, 'management/student_dashboard.html', {'applications': apps})

def internship_list(request):
    # FIXED: Resolves NoReverseMatch for internship_detail
    jobs = Internship.objects.all().order_by('-posted_date')
    return render(request, 'management/internship_list.html', {'internships': jobs})

def internship_detail(request, pk):
    job = get_object_or_404(Internship, pk=pk)
    return render(request, 'management/internship_detail.html', {'internship': job})

def logout_view(request):
    logout(request)
    return redirect('home')