from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Listing, ListingImage


@receiver(post_save, sender=Listing)
def listing_post_save(sender, instance, created, **kwargs):
    """
    Signal fired after a listing is saved
    """
    if created:
        print(f"New listing created: {instance.title}")
        # TODO: Notify users with saved searches
        # from apps.marketplace.tasks import notify_saved_search_users
        # notify_saved_search_users.delay(instance.id)
    else:
        # Check if status changed to sold
        if instance.status == 'sold' and instance.sold_at is None:
            instance.sold_at = timezone.now()
            instance.save(update_fields=['sold_at'])


@receiver(pre_save, sender=Listing)
def listing_pre_save(sender, instance, **kwargs):
    """
    Signal fired before a listing is saved
    """
    # Auto-set expiration date if not set
    if not instance.expires_at and instance.status == 'active':
        from datetime import timedelta
        from django.conf import settings
        instance.expires_at = timezone.now() + timedelta(
            days=settings.LISTING_EXPIRY_DAYS
        )


@receiver(post_save, sender=ListingImage)
def listing_image_post_save(sender, instance, created, **kwargs):
    """
    Signal fired after a listing image is saved
    """
    if created:
        print(f"New image added to listing: {instance.listing.title}")
        # TODO: Process image (resize, create thumbnails) using Celery
        # from apps.marketplace.tasks import process_listing_image
        # process_listing_image.delay(instance.id)