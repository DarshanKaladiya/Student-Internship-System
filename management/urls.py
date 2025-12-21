from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_landing, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Matching views.register_view exactly
    path('register/student/', views.register_view, name='register'),
    path('register/faculty/', views.faculty_register_view, name='faculty_register'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('internships/', views.internship_list, name='internship_list'),
    path('internship/<int:pk>/', views.internship_detail, name='internship_detail'),
    path('update-status/<int:app_id>/<str:new_status>/', views.update_status, name='update_status'),
]