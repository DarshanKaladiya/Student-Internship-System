from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Internship, Application, UserProfile

# --- Home & Auth ---
def home_landing(request):
    context = {
        'total_internships': Internship.objects.count(),
        'total_students': UserProfile.objects.filter(role='STUDENT').count(),
        'total_companies': Internship.objects.values('company_name').distinct().count(),
        'recent_listings': Internship.objects.all().order_by('-posted_date')[:4],
        'current_date': timezone.now(),
    }
    return render(request, 'management/home.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # FIXED: Ensure profile exists
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'STUDENT'})
            return redirect('home')
    return render(request, 'management/login.html', {'form': AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'STUDENT'})
            login(request, user)
            return redirect('home')
    return render(request, 'management/register.html', {'form': UserCreationForm()})

def faculty_register_view(request):
    # Your registration logic here
    return render(request, 'management/faculty_register.html')

# --- Profile Logic ---
@login_required
def student_profile(request):
    # FIXED: Automatically creates profile if missing
    profile, created = UserProfile.objects.get_or_create(user=request.user, defaults={'role': 'STUDENT'})
    
    # Progress bar logic using new fields
    fields = [profile.full_name, profile.roll_no, profile.department, profile.semester, profile.skills]
    filled = [f for f in fields if f and f != ""]
    completion = int((len(filled) / len(fields)) * 100) if fields else 0
    
    return render(request, 'management/profile.html', {
        'profile': profile, 
        'completion': completion
    })

# --- Internship Ops ---
def internship_list(request):
    internships = Internship.objects.all().order_by('-posted_date')
    return render(request, 'management/internship_list.html', {'internships': internships})

def internship_detail(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id)
    return render(request, 'management/internship_detail.html', {'internship': internship})

@login_required
def apply_internship(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id)
    Application.objects.get_or_create(student=request.user, internship=internship)
    return redirect('student_dashboard')

# --- Dashboards ---
@login_required
def student_dashboard(request):
    # FIXED: Use 'applied_on' field
    apps = Application.objects.filter(student=request.user).order_by('-applied_on')
    return render(request, 'management/dashboard.html', {'applications': apps})

@login_required
def faculty_dashboard(request):
    # FIXED: Use 'applied_on' field
    apps = Application.objects.all().order_by('-applied_on')
    return render(request, 'management/faculty_dashboard.html', {'applications': apps})

@login_required
def update_status(request, app_id, new_status):
    application = get_object_or_404(Application, id=app_id)
    application.status = new_status
    application.save()
    return redirect('faculty_dashboard')