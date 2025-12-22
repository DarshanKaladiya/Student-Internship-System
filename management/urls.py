from django.urls import path
from . import views

urlpatterns = [
    # Dashboard & Discovery
    path('', views.home_landing, name='home'),
    path('internships/', views.internship_list, name='internship_list'),
    path('internship/<int:pk>/', views.internship_detail, name='internship_detail'),
    
    # Auth Module
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/student/', views.student_register, name='register'),
    path('register/faculty/', views.faculty_register, name='faculty_register'),
    
    # Signal Logic
    path('profile/', views.student_profile, name='student_profile'), # Fixes image_58f3e0.png
    path('apply/<int:pk>/', views.apply_internship, name='apply_internship'),
    path('review/<int:pk>/<str:status>/', views.review_application, name='review_application'),
    
    # Dashboards
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('post/', views.post_internship, name='post_internship'),
]