import uuid
from django.db import models
from django.utils import timezone


class Conversation(models.Model):
    """Conversation threads between users"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(
        'marketplace.Listing',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversations'
    )
    participant_1 = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='conversations_as_participant_1'
    )
    participant_2 = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='conversations_as_participant_2'
    )
    last_message_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'conversations'
        unique_together = ['participant_1', 'participant_2']
        indexes = [
            models.Index(fields=['listing']),
            models.Index(fields=['participant_1']),
            models.Index(fields=['participant_2']),
            models.Index(fields=['-last_message_at']),
        ]
    
    def __str__(self):
        return f"Conversation: {self.participant_1.username} - {self.participant_2.username}"
    
    def get_other_participant(self, user):
        """Get the other participant in the conversation"""
        if self.participant_1 == user:
            return self.participant_2
        return self.participant_1


class Message(models.Model):
    """Individual messages"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    message_text = models.TextField()
    is_read = models.BooleanField(default=False)
    is_deleted_by_sender = models.BooleanField(default=False)
    is_deleted_by_receiver = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation']),
            models.Index(fields=['sender']),
            models.Index(fields=['receiver']),
            models.Index(fields=['conversation', 'created_at']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"
    
    def mark_as_read(self):
        """Mark message as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])