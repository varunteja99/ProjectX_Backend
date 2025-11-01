from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Conversation


@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, **kwargs):
    """
    Signal fired after a message is saved
    """
    if created:
        # Update conversation's last_message_at
        conversation = instance.conversation
        conversation.last_message_at = timezone.now()
        conversation.save(update_fields=['last_message_at'])
        
        print(f"New message from {instance.sender.username} to {instance.receiver.username}")
        
        # TODO: Send notification to receiver using Celery
        # from apps.messaging.tasks import send_message_notification
        # send_message_notification.delay(instance.id)