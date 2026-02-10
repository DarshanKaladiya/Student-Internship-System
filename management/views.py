from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Internship, Application

# --- AUTHENTICATION ENGINE ---

def login_view(request):
    if request.method == 'POST':
        u, p = request.POST.get('username'), request.POST.get('password')
        mode = request.POST.get('portal_mode')
        
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            try:
                user_profile = user.userprofile
                if user_profile.role == mode:
                    login(request, user)
                    messages.success(request, f"SYNC_START: Identity Verified. Welcome {u}.")
                    
                    # ROLE-BASED REDIRECTION
                    if user_profile.role == 'STUDENT':
                        return redirect('student_dashboard')
                    elif user_profile.role == 'FACULTY':
                        return redirect('faculty_dashboard')
                else:
                    messages.error(request, "ACCESS_DENIED: Role mismatch for selected portal.")
            except UserProfile.DoesNotExist:
                messages.error(request, "SYSTEM_ERROR: User profile data corrupted.")
        else:
            messages.error(request, "INVALID_CIPHER: Credentials mismatch.")
            
    return render(request, 'management/login.html')

def logout_user(request):
    logout(request)
    messages.info(request, "SYNC_TERMINATED: Session ended safely.")
    return redirect('home_landing')

def student_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='STUDENT')
            messages.success(request, "IDENTITY_CREATED: Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'management/register.html', {'form': form})

def faculty_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='FACULTY')
            messages.success(request, "COMMAND_ID_CREATED: Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'management/faculty_register.html', {'form': form})

# --- DASHBOARD & PROFILE SYSTEMS ---

@login_required
def faculty_dashboard(request):
    posted = Internship.objects.filter(faculty=request.user)
    apps = Application.objects.filter(internship__faculty=request.user)
    return render(request, 'management/faculty_dashboard.html', {
        'posted_internships': posted,
        'applications': apps
    })

@login_required
def student_dashboard(request):
    apps = Application.objects.filter(student=request.user)
    return render(request, 'management/student_dashboard.html', {'applications': apps})

@login_required
def faculty_edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name')
        profile.phone_number = request.POST.get('phone_number')
        profile.office_location = request.POST.get('office_location')
        profile.research_interest = request.POST.get('research_interest')
        profile.bio = request.POST.get('bio')
        profile.save()
        messages.success(request, "PROFILE_SYNC: Identity updated.")
        return redirect('faculty_dashboard')
    return render(request, 'management/edit_faculty_profile.html', {'profile': profile})

@login_required
def student_edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name')
        profile.major = request.POST.get('major')
        profile.skills = request.POST.get('skills')
        profile.save()
        messages.success(request, "PROFILE_SYNC: Dossier updated.")
        return redirect('student_dashboard')
    return render(request, 'management/edit_profile.html', {'profile': profile})

# --- INTERNSHIP & NODE MANAGEMENT ---

def internship_list(request):
    nodes = Internship.objects.all().order_by('-created_at')
    return render(request, 'management/internship_list.html', {'internships': nodes})

def internship_detail(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    return render(request, 'management/internship_detail.html', {'internship': internship})

@login_required
def post_internship(request):
    if request.method == 'POST':
        Internship.objects.create(
            faculty=request.user,
            title=request.POST.get('title'),
            company_name=request.POST.get('company_name'),
            stipend=request.POST.get('stipend'),
            location=request.POST.get('location'),
            description=request.POST.get('description'),
            required_skills=request.POST.get('required_skills'),
            deadline=request.POST.get('deadline'),
            external_apply_link=request.POST.get('external_apply_link') # GOOGLE FORM LINK
        )
        messages.success(request, "NODE_DEPLOYED: Internship is live in the network.")
        return redirect('faculty_dashboard')
    return render(request, 'management/post_internship.html')

@login_required
def apply_internship(request, pk):
    node = get_object_or_404(Internship, pk=pk)
    Application.objects.get_or_create(student=request.user, internship=node)
    messages.success(request, "SIGNAL_SENT: Application transmitted to faculty.")
    return redirect('student_dashboard')

# --- APPLICATION WORKFLOW ---

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
    application = get_object_or_404(Application, student__pk=student_pk, internship__pk=internship_pk)
    return render(request, 'management/view_profile.html', {
        'profile': student_profile,
        'application': application,
        'internship': application.internship
    })

def home_landing(request):
    return render(request, 'management/home.html')