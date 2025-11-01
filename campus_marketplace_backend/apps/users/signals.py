from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """
    Signal fired after a user is saved
    """
    if created:
        # User was just created
        print(f"New user created: {instance.email}")
        # TODO: Send welcome email using Celery
        # from apps.users.tasks import send_welcome_email
        # send_welcome_email.delay(instance.id)
    else:
        # User was updated
        print(f"User updated: {instance.email}")