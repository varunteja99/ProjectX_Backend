from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review


@receiver(post_save, sender=Review)
def review_post_save(sender, instance, created, **kwargs):
    """
    Signal fired after a review is saved
    """
    if created:
        print(f"New review: {instance.rating} stars for {instance.reviewee.username}")
        
        # Update reviewee's rating
        instance.reviewee.update_rating()
        
        # TODO: Notify reviewee using Celery
        # from apps.reviews.tasks import send_review_notification
        # send_review_notification.delay(instance.id)


@receiver(post_delete, sender=Review)
def review_post_delete(sender, instance, **kwargs):
    """
    Signal fired after a review is deleted
    """
    # Recalculate reviewee's rating
    instance.reviewee.update_rating()
    print(f"Review deleted for {instance.reviewee.username}")