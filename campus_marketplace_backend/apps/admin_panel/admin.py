from django.contrib import admin
from .models import SystemSetting, ActivityLog


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ['setting_key', 'setting_type', 'is_public', 'updated_at']
    list_filter = ['setting_type', 'is_public']
    search_fields = ['setting_key', 'description']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action_type', 'entity_type', 'created_at']
    list_filter = ['action_type', 'entity_type', 'created_at']
    search_fields = ['user__username', 'action_type']
    readonly_fields = ['created_at']