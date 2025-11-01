from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Transaction, Offer


@receiver(post_save, sender=Offer)
def offer_post_save(sender, instance, created, **kwargs):
    """
    Signal fired after an offer is saved
    """
    if created:
        print(f"New offer: ${instance.offer_amount} for {instance.listing.title}")
        # TODO: Notify seller using Celery
        # from apps.transactions.tasks import send_offer_notification
        # send_offer_notification.delay(instance.id)
    else:
        # Offer status changed
        if instance.status == 'accepted':
            print(f"Offer accepted: ${instance.offer_amount}")
            # TODO: Notify buyer
            # from apps.transactions.tasks import send_offer_accepted_notification
            # send_offer_accepted_notification.delay(instance.id)


@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, created, **kwargs):
    """
    Signal fired after a transaction is saved
    """
    if created:
        print(f"New transaction created for: {instance.listing.title}")
    else:
        # Check if status changed to completed
        if instance.status == 'completed' and not instance.completed_at:
            instance.completed_at = timezone.now()
            instance.save(update_fields=['completed_at'])
            
            # Mark listing as sold
            listing = instance.listing
            if listing.status != 'sold':
                listing.status = 'sold'
                listing.sold_at = timezone.now()
                listing.save(update_fields=['status', 'sold_at'])
            
            print(f"Transaction completed: {instance.listing.title}")
            # TODO: Request reviews from both parties
            # from apps.transactions.tasks import request_reviews
            # request_reviews.delay(instance.id)