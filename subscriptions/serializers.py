from rest_framework import serializers
from subscriptions.models import Subscription, Company, Client, Package
from packages.models import Service
from django.urls import reverse
from utils.constants import SUBSCRIBER_TYPE_INDIVIDUAL
from utils.helpers import create_subcription_invoice
from django_celery_beat.models import PeriodicTask
from invoices.models import Invoice


class SubscriptionSerializer(serializers.ModelSerializer):
    package = serializers.PrimaryKeyRelatedField(
        queryset=Package.objects.all(), required=True, write_only=True)
    payment_url = serializers.SerializerMethodField()
    redirect_url = serializers.URLField(write_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = (
            'status', 'current_invoicing_end_date', 'current_invoicing_start_date')

    def validate(self, attrs):
        attrs = super(SubscriptionSerializer, self).validate(attrs)

        # check if payment for this service exists
        is_non_individual_subscriber = attrs.get(
            'type') != SUBSCRIBER_TYPE_INDIVIDUAL
        if is_non_individual_subscriber:
            subscription_service = attrs.get('package').service
            subscribing_entity = Company.objects.get(ref=attrs.get('ref'))
            service_payment_invoice = subscribing_entity.invoices.filter(
                service=subscription_service).first()
            if not service_payment_invoice or (service_payment_invoice is not None and not service_payment_invoice.paid):
                raise serializers.ValidationError(
                    {'service_subscriptions': "You are not allowed to subscribe for this service no service payment has been made"},
                    "subscription_failed")

        return attrs

    def get_payment_url(self, instance):
        recent_invoice = instance.recent_invoice()
        if recent_invoice and not recent_invoice.paid:
            return reverse("payment_form", args=[recent_invoice.id])


class SubscriptionRenewalSerializer(serializers.Serializer):
    subscription = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Subscription.objects.all())
    redirect_url = serializers.URLField()

    status = 201

    def save(self):
        renewed_sub = self.validated_data.get('subscription')
        renewed_sub.redirect_url = self.validated_data.get('redirect_url')
        self.instance = create_subcription_invoice(renewed_sub, renew=True)

    def to_representation(self, instance):
        if isinstance(instance, Invoice):
            return {
                "success": True,
                "message": "Subscription renewal invoice has been generated",
                "subscription": SubscriptionSerializer(self.validated_data.get('subscription')).data
            }
        elif isinstance(instance, PeriodicTask):
            return {
                "success": True,
                "message": "A renewal request has been acknowledged!. Renewal will be effected at the end of the current subscription period."
            }
        else:
            self.status = 204
            return None


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
