from django.contrib import admin
from subscriptions.models import Subscription, Company, Client

admin.site.register(Subscription)
admin.site.register(Company)
admin.site.register(Client)

