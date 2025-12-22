from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Application, Internship
from django.contrib import messages

# --- LANDING & LISTINGS ---
def home_landing(request):
    """Uses 'posted_date' to resolve FieldError."""
    internships = Internship.objects.all().order_by('-posted_date')[:4]
    return render(request, 'management/home.html', {'internships': internships})

def internship_list(request):
    jobs = Internship.objects.all().order_by('-posted_date')
    return render(request, 'management/internship_list.html', {'internships': jobs})

def internship_detail(request, pk):
    job = get_object_or_404(Internship, pk=pk)
    return render(request, 'management/internship_detail.html', {'internship': job})

# --- AUTHENTICATION WITH ROLE VALIDATION ---
def login_view(request):
    """Strict role-based login with custom alert messages."""
    role_required = request.GET.get('role', 'Student').upper() 
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                try:
                    profile = user.userprofile
                    if profile.role == role_required:
                        login(request, user)
                        messages.success(request, f"Welcome back, {username}!")
                        return redirect('faculty_dashboard' if profile.role == 'FACULTY' else 'student_dashboard')
                    else:
                        # Alert: Wrong role trying to access this portal
                        messages.error(request, f"Access Denied: You are a {profile.role.capitalize()}. Please use the {profile.role.capitalize()} Login.")
                except UserProfile.DoesNotExist:
                    messages.error(request, "Error: Profile not found.")
        else:
            # Alert: Incorrect credentials
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'management/login.html', {'form': form, 'role': role_required.capitalize()})

def register_view(request):
    """Student Registration."""
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

def logout_view(request):
    logout(request)
    return redirect('home')

# --- PROFILE & PORTALS ---
@login_required
def student_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'management/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    """Resolves IntegrityError by handling NULL skills."""
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name', '')
        profile.roll_no = request.POST.get('roll_no', '')
        profile.department = request.POST.get('department', '')
        profile.skills = request.POST.get('skills', '') 
        profile.save()
        messages.success(request, "Profile updated!")
        return redirect('student_profile')
    return render(request, 'management/edit_profile.html', {'profile': profile})

@login_required
def faculty_dashboard(request):
    """Queries applications via User instance."""
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'FACULTY':
        return redirect('home')
    apps = Application.objects.filter(internship__faculty=request.user)
    return render(request, 'management/faculty_dashboard.html', {'applications': apps})

@login_required
def update_status(request, app_id, new_status):
    """Resolves AttributeError in terminal."""
    application = get_object_or_404(Application, id=app_id)
    application.status = new_status
    application.save()
    return redirect('faculty_dashboard')

@login_required
def student_dashboard(request):
    apps = Application.objects.filter(student=request.user).order_by('-applied_on')
    return render(request, 'management/student_dashboard.html', {'applications': apps})

@login_required
def apply_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    if not Application.objects.filter(student=request.user, internship=internship).exists():
        Application.objects.create(student=request.user, internship=internship)
    return redirect('student_dashboard')