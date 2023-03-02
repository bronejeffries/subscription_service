from django.db import models
from packages.models import Package, DatedModel
from utils import constants
from invoices.models import Invoice
from django.contrib.contenttypes.fields import GenericRelation


class Subscription(DatedModel):
    ref = models.CharField(max_length=250, null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    contact = models.CharField(null=True, blank=True, max_length=15)
    extras = models.JSONField(help_text="subscribers details")
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name="package_subscriptions")
    type = models.CharField(
        max_length=25, choices=constants.SUSCRIBER_TYPE_CHOICES, default=constants.SUBSCRIBER_TYPE_NON_INDIVIDUAL)
    status = models.CharField(
        max_length=25, choices=constants.VALIDITY_STATUS_CHOICES, default=constants.VALIDITY_STATUS_PENDING)
    current_invoicing_start_date = models.DateTimeField(null=True, blank=True)
    current_invoicing_end_date = models.DateTimeField(null=True, blank=True)
    invoices = GenericRelation(
        Invoice, content_type_field="content_type",
        object_id_field="object_id", related_query_name="subscription")

    redirect_url = None

    def __init__(self, *args, **kwargs):
        self.redirect_url = kwargs.pop('redirect_url',None)
        super(Subscription, self).__init__(*args, **kwargs)

    def recent_invoice(self):
        return self.invoices.first()

    def is_individual(self):
        return self.type == constants.SUBSCRIBER_TYPE_INDIVIDUAL

    def owning_entity(self):
        return Company.objects.get(ref=self.ref) if not self.is_individual() else None


class Company(DatedModel):
    name = models.CharField(max_length=250, null=False, blank=False)
    ref = models.CharField(max_length=30, null=False, blank=False, unique=True)
    extras = models.JSONField(null=True, blank=True)
    source = models.CharField(max_length=30, null=False, blank=False)

    invoices = GenericRelation(Invoice, object_id_field="owner_id",
                               content_type_field="owner_content_type", related_query_name="company")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"


class Client(DatedModel):
    ref = models.CharField(max_length=30, null=False, unique=True)
    extras = models.JSONField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                to_field="ref", related_name="company_clients")
    is_active = models.BooleanField()
    last_activity_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.ref} {self.company}"
