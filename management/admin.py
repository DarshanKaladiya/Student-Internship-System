from django.contrib import admin
from .models import UserProfile, Internship, Application

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for managing user identities and roles."""
    list_display = ('user', 'full_name', 'role', 'department', 'semester')
    list_filter = ('role', 'department', 'semester')
    search_fields = ('user__username', 'full_name', 'roll_no')
    fieldsets = (
        ('Account Info', {'fields': ('user', 'role')}),
        ('Academic Profile', {'fields': ('full_name', 'roll_no', 'department', 'semester')}),
        ('Professional Data', {'fields': ('skills', 'profile_pic')}),
    )

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    """Admin control for internship nodes and deadline tracking."""
    list_display = ('title', 'faculty', 'company_name', 'location', 'deadline', 'posted_date')
    list_filter = ('location', 'posted_date', 'deadline')
    search_fields = ('title', 'company_name', 'description', 'faculty__username')
    ordering = ('-posted_date',)
    
    # Custom display to show status in admin list
    def is_active(self, obj):
        return obj.days_left() > 0 if obj.deadline else True
    is_active.boolean = True
    is_active.short_description = 'Active Node'

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Admin monitoring for student-faculty synchronization."""
    list_display = ('student', 'internship', 'status', 'applied_date')
    list_filter = ('status', 'applied_date')
    search_fields = ('student__username', 'internship__title')
    actions = ['approve_applications', 'reject_applications']

    def approve_applications(self, request, queryset):
        queryset.update(status='APPROVED')
    approve_applications.short_description = "Mark selected as Approved"

    def reject_applications(self, request, queryset):
        queryset.update(status='REJECTED')
    reject_applications.short_description = "Mark selected as Rejected"