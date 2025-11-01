import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Offer(models.Model):
    """Price negotiation offers"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('countered', 'Countered'),
        ('expired', 'Expired'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(
        'marketplace.Listing',
        on_delete=models.CASCADE,
        related_name='offers'
    )
    buyer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='offers_made'
    )
    seller = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='offers_received'
    )
    offer_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    parent_offer = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='counter_offers'
    )
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'offers'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['listing']),
            models.Index(fields=['buyer']),
            models.Index(fields=['seller']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Offer ${self.offer_amount} for {self.listing.title}"


class Transaction(models.Model):
    """Transaction tracking"""
    
    STATUS_CHOICES = [
        ('inquired', 'Inquired'),
        ('negotiating', 'Negotiating'),
        ('sold', 'Sold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(
        'marketplace.Listing',
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    buyer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    seller = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='sales'
    )
    offer = models.ForeignKey(
        Offer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transaction'
    )
    final_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inquired')
    meeting_location = models.CharField(max_length=255, blank=True)
    meeting_time = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['listing']),
            models.Index(fields=['buyer']),
            models.Index(fields=['seller']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Transaction for {self.listing.title}"


class MeetingLocation(models.Model):
    """Safe meeting locations"""
    
    LOCATION_TYPE_CHOICES = [
        ('library', 'Library'),
        ('student_center', 'Student Center'),
        ('security_desk', 'Security Desk'),
        ('cafeteria', 'Cafeteria'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campus = models.ForeignKey(
        'marketplace.Campus',
        on_delete=models.CASCADE,
        related_name='meeting_locations'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location_type = models.CharField(max_length=50, choices=LOCATION_TYPE_CHOICES)
    address = models.TextField(blank=True)
    building = models.CharField(max_length=100, blank=True)
    room_number = models.CharField(max_length=50, blank=True)
    hours_of_operation = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'meeting_locations'
        indexes = [
            models.Index(fields=['campus']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.campus.name}"