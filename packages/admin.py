from django.contrib import admin

from packages.models import Period, Package, Service, Currency

admin.site.register(Period)
admin.site.register(Package)
admin.site.register(Service)
admin.site.register(Currency)
