import uuid
from django.db import models
from django.utils import timezone


class SystemSetting(models.Model):
    """System-wide configuration settings"""
    
    SETTING_TYPE_CHOICES = [
        ('string', 'String'),
        ('integer', 'Integer'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    setting_key = models.CharField(max_length=100, unique=True)
    setting_value = models.TextField(blank=True)
    setting_type = models.CharField(max_length=50, choices=SETTING_TYPE_CHOICES)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'system_settings'
        indexes = [
            models.Index(fields=['setting_key']),
        ]
    
    def __str__(self):
        return self.setting_key


class ActivityLog(models.Model):
    """User activity tracking"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activity_logs'
    )
    action_type = models.CharField(max_length=100)
    entity_type = models.CharField(max_length=50, blank=True)
    entity_id = models.UUIDField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    details = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'activity_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['action_type']),
            models.Index(fields=['entity_type']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.action_type} - {self.user}"