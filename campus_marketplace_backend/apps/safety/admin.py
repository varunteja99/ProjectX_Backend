from django.contrib import admin
from .models import FlaggedContent, Dispute, DisputeEvidence, BlockedUser, Notification, StudyMaterial


@admin.register(FlaggedContent)
class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'reporter', 'reason', 'status', 'created_at']
    list_filter = ['content_type', 'reason', 'status', 'created_at']
    search_fields = ['reporter__username', 'description']


@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'complainant', 'respondent', 'dispute_type', 'status', 'created_at']
    list_filter = ['dispute_type', 'status', 'created_at']
    search_fields = ['complainant__username', 'respondent__username', 'description']


@admin.register(DisputeEvidence)
class DisputeEvidenceAdmin(admin.ModelAdmin):
    list_display = ['dispute', 'submitted_by', 'evidence_type', 'created_at']
    list_filter = ['evidence_type', 'created_at']


@admin.register(BlockedUser)
class BlockedUserAdmin(admin.ModelAdmin):
    list_display = ['blocker', 'blocked', 'created_at']
    search_fields = ['blocker__username', 'blocked__username']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploader', 'campus', 'material_type', 'course_code', 'is_approved']
    list_filter = ['material_type', 'is_approved', 'campus']
    search_fields = ['title', 'course_code', 'course_name']