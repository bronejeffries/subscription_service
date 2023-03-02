from rest_framework import serializers
from packages.models import Package, Service, Period, Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(required=False)

    class Meta:
        model = Service
        fields = '__all__'


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'


class PackageSerializer(serializers.ModelSerializer):
    period = PeriodSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = Package
        fields = '__all__'
