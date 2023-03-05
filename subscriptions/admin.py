from django.contrib import admin
from subscriptions.models import Subscription, Company, Client


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('package', 'owner', 'ref', 'type', 'status',
                    'current_invoicing_start_date', 'current_invoicing_end_date')
    list_filter = ('type', 'package')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'source', 'ref')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'extras',
                    'is_active', 'last_activity_date')
