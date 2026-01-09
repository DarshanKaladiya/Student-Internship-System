from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_landing, name='home_landing'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.student_register, name='register'),
    path('faculty-register/', views.faculty_register, name='faculty_register'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('profile/edit/', views.student_edit_profile, name='student_edit_profile'),
    # Comparison View URL
    path('profile/view/<int:student_pk>/<int:internship_pk>/', views.view_student_profile, name='view_student_profile'),
    path('post/', views.post_internship, name='post_internship'),
    path('internships/', views.internship_list, name='internship_list'),
    path('internships/<int:pk>/', views.internship_detail, name='internship_detail'),
    path('apply/<int:pk>/', views.apply_internship, name='apply_internship'),
    path('application-sent/', views.application_success, name='application_success'),
    path('approve/<int:pk>/', views.approve_application, name='approve_application'),
    path('reject/<int:pk>/', views.reject_application, name='reject_application'),
]