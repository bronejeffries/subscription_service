from django.db import models
from utils.models import DatedModel
from utils.constants import INVOICE_TYPE_CHOICES, PAYMENT_MERCHANT_AIRTEL, PAYMENT_MERCHANT_MTN
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Invoice(DatedModel):
    type = models.CharField(max_length=35, choices=INVOICE_TYPE_CHOICES)
    # billing period details
    effective_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    amount = models.FloatField(null=False, blank=False)

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="invoice_object_content")
    content_object = GenericForeignKey('content_type', 'object_id')

    owner_id = models.PositiveIntegerField(null=True, blank=True)
    owner_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    owner = GenericForeignKey('owner_content_type', 'owner_id')

    paid = models.BooleanField(default=False)

    # redirect_url
    redirect_url = models.URLField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            models.Index(fields=["owner_content_type", "owner_id"])
        ]

    def __str__(self):
        return f"{self.get_type_display()} invoice for {self.owner}"

    def billed_period_expired(self):
        return False


class MobilePaymentProvider(DatedModel):
    name = models.CharField(
        choices=(
            (PAYMENT_MERCHANT_AIRTEL, "AIRTEL"),
            (PAYMENT_MERCHANT_MTN, "MTN")
        ), max_length=50)


class Payment(DatedModel):
    amount = models.FloatField(blank=False, null=False)
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="payments", null=True)

    provider_id = models.PositiveIntegerField(null=False, blank=False)
    provider_content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    payment_provider = GenericForeignKey(
        'provider_content_type', 'provider_id')
