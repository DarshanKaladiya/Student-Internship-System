from django.urls import path
from . import views

urlpatterns = [
    # Dashboard and Home
    path('', views.home_landing, name='home'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 
    path('register/student/', views.register_view, name='register'),
    path('register/faculty/', views.faculty_register_view, name='faculty_register'),
    
    # Profile and Internships
    path('profile/', views.student_profile, name='student_profile'),
    path('internships/', views.internship_list, name='internship_list'),
    path('internship/<int:internship_id>/', views.internship_detail, name='internship_detail'),
    path('apply/<int:internship_id>/', views.apply_internship, name='apply_internship'),
    
    # Dashboards and Actions
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('update-status/<int:app_id>/<str:new_status>/', views.update_status, name='update_status'),
]