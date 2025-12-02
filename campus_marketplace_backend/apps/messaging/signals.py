from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Conversation
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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
        
        # Broadcast to WebSocket group
        channel_layer = get_channel_layer()
        room_group_name = f'chat_{conversation.id}'
        
        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'type': 'chat_message',
                'message': instance.message_text,
                'sender_id': str(instance.sender.id),
                'sender_username': instance.sender.username,
                'created_at': instance.created_at.isoformat(),
                'id': str(instance.id)
            }
        )
        
        # TODO: Send notification to receiver using Celery
        # from apps.messaging.tasks import send_message_notification
        # send_message_notification.delay(instance.id)