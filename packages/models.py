from django.db import models
from utils.models import DatedModel
from utils import constants
from invoices.models import Invoice
from django.contrib.contenttypes.fields import GenericRelation


class Currency(DatedModel):
    name = models.CharField(max_length=25, null=False, blank=False, unique=True)
    symbol = models.CharField(max_length=20, null=False, blank=False)
    rate = models.FloatField(null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Currencies"


class Service(DatedModel):
    name = models.CharField(max_length=25, blank=True, null=False)
    description = models.TextField(max_length=300, null=False, blank=False)
    amount = models.FloatField(default=0)
    currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True, blank=True)
    invoices = GenericRelation(
        Invoice, content_type_field="content_type",
        object_id_field="object_id", related_query_name="service")

    def __str__(self):
        return self.name


class Period(DatedModel):
    name = models.CharField(max_length=25, blank=False, null=False)
    description = models.TextField(max_length=300, null=True, blank=True)
    validity_unit = models.CharField(
        max_length=25, choices=constants.VALIDITY_UNIT_CHOICES, default=constants.VALIDITY_UNIT_DAYS)
    validity_span = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name



class Package(DatedModel):
    service = models.ForeignKey(Service, on_delete=models.CASCADE,null=True)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    rate = models.FloatField(null=False, blank=False,
                             help_text="package billing rate")
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, null=True, blank=True)
    billing_model = models.CharField(
        max_length=30, choices=constants.BILLING_MODEL_CHOICES, default=constants.BILLING_MODEL_FLAT_RATE)
    billing_unit_limit = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return f"{self.service} {self.period} {self.rate}"
