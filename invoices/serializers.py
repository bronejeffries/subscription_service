from django.urls import reverse
from django.utils.http import urlencode
from generic_relations.relations import GenericRelatedField
from rest_framework import serializers

from invoices.models import Invoice
from packages.serializers import Service, ServiceSerializer
from subscriptions.serializers import (Company, CompanySerializer,
                                       Subscription, SubscriptionSerializer)
from utils.constants import INVOICE_TYPE_SERVICE


class ServicePaymentSerializer(serializers.Serializer):
    service = serializers.PrimaryKeyRelatedField(many=False,
                                                 required=True, queryset=Service.objects.all())
    company = serializers.SlugRelatedField(slug_field="ref",
                                           queryset=Company.objects.all(), required=True)
    redirect_url = serializers.URLField(required=True)

    class Meta:
        fields = ('service', 'company', 'redirect_url')

    def save(self, **kwargs):
        # create payment service invoice
        defaults = {
            'amount': self.validated_data.get('service').amount,
            'redirect_url': self.validated_data.get('redirect_url')
        }
        invoice = Invoice.objects.create(type=INVOICE_TYPE_SERVICE,
                                         content_object=self.validated_data.get(
                                             'service'),
                                         owner=self.validated_data.get(
                                             'company'),
                                         **defaults)
        self.instance = invoice
        return self.instance

    def to_representation(self, instance):
        return {
            "success": True,
            "message": "Service Invoice Created Successfuly",
            "redirect_url": reverse("payment_form", args=[instance.id])
        }

class InvoiceSerializer(serializers.ModelSerializer):
    
    owner = GenericRelatedField(
        {
            Company: CompanySerializer()
        }
    )
    invoiced_object = GenericRelatedField({
        Service: ServiceSerializer(),
        Subscription: SubscriptionSerializer()
    }, source="content_object")
    
    class Meta:
        model = Invoice
        exclude = ('owner_id','owner_content_type','content_type','object_id')