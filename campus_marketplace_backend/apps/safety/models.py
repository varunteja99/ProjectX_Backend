import uuid
from django.db import models
from django.utils import timezone


class FlaggedContent(models.Model):
    """Reported inappropriate content"""
    
    CONTENT_TYPE_CHOICES = [
        ('listing', 'Listing'),
        ('message', 'Message'),
        ('user', 'User'),
        ('review', 'Review'),
    ]
    
    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('offensive', 'Offensive Content'),
        ('scam', 'Scam/Fraud'),
        ('inappropriate', 'Inappropriate'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reporter = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='reports_made'
    )
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES)
    content_id = models.UUIDField()
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports_reviewed'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    action_taken = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'flagged_content'
        indexes = [
            models.Index(fields=['reporter']),
            models.Index(fields=['content_type']),
            models.Index(fields=['content_id']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Report: {self.content_type} - {self.reason}"


class Dispute(models.Model):
    """Transaction dispute management"""
    
    DISPUTE_TYPE_CHOICES = [
        ('item_not_as_described', 'Item Not As Described'),
        ('no_show', 'No Show'),
        ('payment_issue', 'Payment Issue'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_review', 'In Review'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(
        'transactions.Transaction',
        on_delete=models.CASCADE,
        related_name='disputes'
    )
    complainant = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='disputes_filed'
    )
    respondent = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='disputes_against'
    )
    dispute_type = models.CharField(max_length=50, choices=DISPUTE_TYPE_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    resolution = models.TextField(blank=True)
    resolved_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='disputes_resolved'
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'disputes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transaction']),
            models.Index(fields=['complainant']),
            models.Index(fields=['respondent']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Dispute: {self.dispute_type} - {self.transaction.listing.title}"


class DisputeEvidence(models.Model):
    """Evidence submitted for disputes"""
    
    EVIDENCE_TYPE_CHOICES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('screenshot', 'Screenshot'),
        ('message', 'Message'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dispute = models.ForeignKey(
        Dispute,
        on_delete=models.CASCADE,
        related_name='evidence'
    )
    submitted_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='evidence_submitted'
    )
    evidence_type = models.CharField(max_length=50, choices=EVIDENCE_TYPE_CHOICES)
    file_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'dispute_evidence'
        indexes = [
            models.Index(fields=['dispute']),
            models.Index(fields=['submitted_by']),
        ]
    
    def __str__(self):
        return f"Evidence for {self.dispute}"


class BlockedUser(models.Model):
    """Users blocking other users"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blocker = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='users_blocked'
    )
    blocked = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='blocked_by_users'
    )
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'blocked_users'
        unique_together = ['blocker', 'blocked']
        indexes = [
            models.Index(fields=['blocker']),
            models.Index(fields=['blocked']),
        ]
    
    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked.username}"


class Notification(models.Model):
    """User notifications"""
    
    NOTIFICATION_TYPE_CHOICES = [
        ('message', 'New Message'),
        ('offer', 'New Offer'),
        ('status_change', 'Status Change'),
        ('price_drop', 'Price Drop'),
        ('listing_expiring', 'Listing Expiring'),
        ('review', 'New Review'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    reference_id = models.UUIDField(null=True, blank=True)
    reference_type = models.CharField(max_length=50, blank=True)
    is_read = models.BooleanField(default=False)
    is_pushed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['user', 'is_read', '-created_at']),
        ]
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])


class StudyMaterial(models.Model):
    """Academic materials shared by students"""
    
    MATERIAL_TYPE_CHOICES = [
        ('notes', 'Class Notes'),
        ('study_guide', 'Study Guide'),
        ('practice_exam', 'Practice Exam'),
        ('syllabus', 'Syllabus'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploader = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='study_materials_uploaded'
    )
    campus = models.ForeignKey(
        'marketplace.Campus',
        on_delete=models.CASCADE,
        related_name='study_materials'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    course_code = models.CharField(max_length=50, blank=True)
    course_name = models.CharField(max_length=255, blank=True)
    material_type = models.CharField(max_length=50, choices=MATERIAL_TYPE_CHOICES)
    file_url = models.URLField(blank=True, null=True)
    file_size = models.IntegerField(null=True, blank=True, help_text="File size in bytes")
    file_type = models.CharField(max_length=50, blank=True)
    download_count = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'study_materials'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['uploader']),
            models.Index(fields=['campus']),
            models.Index(fields=['course_code']),
            models.Index(fields=['material_type']),
            models.Index(fields=['is_approved']),
        ]
    
    def __str__(self):
        return self.title
    
    def increment_download_count(self):
        """Increment download count"""
        self.download_count += 1
        self.save(update_fields=['download_count'])