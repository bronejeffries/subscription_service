from django.contrib import admin
from invoices.models import Invoice
# Register your models here.

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('type','owner','amount','paid','effective_date','end_date')
    list_filter = ('type','paid','effective_date','end_date')
    readonly_fields = ('object_id','content_type','owner_id','owner_content_type')

