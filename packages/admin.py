from django.contrib import admin

from packages.models import Period, Package, Service, Currency

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('name','description','validity_unit','validity_span')
  
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('service','period','rate','currency','billing_model','billing_unit_limit')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name','description','amount','currency')

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name','symbol','rate')