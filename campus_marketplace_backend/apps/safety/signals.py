from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FlaggedContent, Dispute, Notification


@receiver(post_save, sender=FlaggedContent)
def flagged_content_post_save(sender, instance, created, **kwargs):
    """
    Signal fired after content is flagged
    """
    if created:
        print(f"Content flagged: {instance.content_type} - {instance.reason}")
        # TODO: Notify admins using Celery
        # from apps.safety.tasks import notify_admins_flagged_content
        # notify_admins_flagged_content.delay(instance.id)


@receiver(post_save, sender=Dispute)
def dispute_post_save(sender, instance, created, **kwargs):
    """
    Signal fired after a dispute is saved
    """
    if created:
        print(f"New dispute filed: {instance.dispute_type}")
        # TODO: Notify admins and respondent using Celery
        # from apps.safety.tasks import notify_dispute_parties
        # notify_dispute_parties.delay(instance.id)
    else:
        # Check if dispute was resolved
        if instance.status == 'resolved' and instance.resolved_at:
            print(f"Dispute resolved: {instance.id}")
            # TODO: Notify both parties
            # from apps.safety.tasks import notify_dispute_resolved
            # notify_dispute_resolved.delay(instance.id)


@receiver(post_save, sender=Notification)
def notification_post_save(sender, instance, created, **kwargs):
    """
    Signal fired after a notification is saved
    """
    if created and not instance.is_pushed:
        print(f"New notification for {instance.user.username}: {instance.title}")
        # TODO: Send push notification using Celery
        # from apps.safety.tasks import send_push_notification
        # send_push_notification.delay(instance.id)