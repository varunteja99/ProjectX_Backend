from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'campus', 'is_verified', 'account_status']
    list_filter = ['is_verified', 'is_active', 'account_status', 'campus']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture_url', 'student_id')}),
        ('Campus', {'fields': ('campus',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'account_status')}),
        ('Ratings', {'fields': ('average_rating', 'total_reviews')}),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )