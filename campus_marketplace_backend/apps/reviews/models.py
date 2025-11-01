import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """User ratings and reviews"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.OneToOneField(
        'transactions.Transaction',
        on_delete=models.CASCADE,
        related_name='review'
    )
    reviewer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='reviews_given'
    )
    reviewee = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='reviews_received'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField(blank=True)
    is_buyer_review = models.BooleanField(
        help_text="True if buyer reviewing seller, False if seller reviewing buyer"
    )
    is_flagged = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reviews'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reviewer']),
            models.Index(fields=['reviewee']),
            models.Index(fields=['reviewee', 'rating']),
        ]
    
    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewee.username}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update reviewee's rating
        self.reviewee.update_rating()