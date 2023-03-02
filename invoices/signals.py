from django.db.models.signals import post_save
from django.dispatch import receiver
from invoices.models import Invoice, Payment
from utils.constants import VALIDITY_STATUS_PENDING, VALIDITY_STATUS_ACTIVE
from subscriptions.models import Subscription
from django.db.models import Sum, FloatField


@receiver(post_save, sender=Invoice)
def handle_invoice_save(sender, instance, created=False, **kwargs):
    if not created:
        if instance.paid and isinstance(instance.content_object, Subscription):
            subscription = instance.content_object
            subscription.status = VALIDITY_STATUS_ACTIVE
            subscription.save()


@receiver(post_save, sender=Payment)
def handle_payment(sender, instance, created=False, **kwargs):
    if created:
        payment_invoice = instance.invoice
        invoice_amount_paid = payment_invoice.payments.aggregate(
            amount_paid=Sum('amount', output_field=FloatField())
        )['amount_paid']
        if invoice_amount_paid == payment_invoice.amount:
            payment_invoice.paid = True
            payment_invoice.save()
