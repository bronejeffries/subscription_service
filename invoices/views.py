from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from utils.constants import PAYMENT_MERCHANT_AIRTEL, PAYMENT_MERCHANT_MTN
from rest_framework.viewsets import ReadOnlyModelViewSet
from invoices.serializers import InvoiceSerializer, Invoice
from rest_framework.permissions import IsAuthenticated

class InvoiceViewSet(ReadOnlyModelViewSet):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    permission_classes = [IsAuthenticated]

class PaymentTemplateView(TemplateView):
    template_name = "invoices/payment_form.html"

    def get_object(self, **kwargs):
        return get_object_or_404(Invoice, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["invoice"] = self.get_object(id=kwargs['invoice'])
        return context

    # handle payment submission
    def post(self, request, invoice, **kwargs):

        payment_merchant = request.POST.get('payment_merchant')
        if payment_merchant == PAYMENT_MERCHANT_AIRTEL:
            pass

        if payment_merchant == PAYMENT_MERCHANT_MTN:
            pass
        obj = self.get_object(id=invoice)
        return redirect(obj.redirect_url)
