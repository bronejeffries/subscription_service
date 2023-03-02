from subscriptions.models import Subscription
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.helpers import create_subcription_invoice

@receiver(post_save, sender=Subscription)
def create_subscription_invoice(sender, instance, created=False, **kwargs):
    if created:
        create_subcription_invoice(instance)