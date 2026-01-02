from django.contrib import admin
from .models import UserProfile, Internship, Application


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'company_name',
        'faculty',
        'location',
        'stipend',
        'deadline',
    )
    list_filter = ('location', 'deadline')
    search_fields = ('title', 'company_name', 'required_skills')
    ordering = ('deadline',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'internship',
        'status',
    )
    list_filter = ('status',)
    search_fields = ('student__username', 'internship__title')
