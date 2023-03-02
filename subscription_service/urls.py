"""subscription_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from subscriptions.views import SubscriptionViewSet, CompanyViewSet, ClientViewSet
from packages.views import PackageViewSet, ServiceViewSet, PeriodViewSet
from invoices.views import PaymentTemplateView, InvoiceViewSet
from rest_framework.routers import DefaultRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Subscription Service API",
        default_version='v1',
        description="Subscription Service",
        #   terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ssematebrian2067@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'periods', PeriodViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('initiate_payment/<int:invoice>/',
         PaymentTemplateView.as_view(), name="payment_form"),
    path('api/', include(router.urls)),
    path('docs', schema_view.with_ui('redoc', cache_timeout=0)),
    path('', include('admin_soft.urls'))
]
