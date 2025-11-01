from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import ActivityLog

User = get_user_model()


@receiver(post_save, sender=User)
def log_user_activity(sender, instance, created, **kwargs):
    """
    Log user registration activity
    """
    if created:
        ActivityLog.objects.create(
            user=instance,
            action_type='user_registered',
            entity_type='user',
            entity_id=instance.id,
            details={'email': instance.email, 'username': instance.username}
        )
        print(f"Activity logged: User registered - {instance.email}")