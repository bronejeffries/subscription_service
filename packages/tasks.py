from subscription_service import celery_app
from utils.helpers import create_subcription_invoice
from packages.models import Package
from utils.constants import VALIDITY_STATUS_ACTIVE
from django.utils import timezone
from django.db.models import Q


@celery_app.task
def manage_package_subscriptions(package_validity_unit):
    """
    invoices/update validity for active subscriptions
    re-runs on intervals depending on the validity unit
    Args:
        package_validity_unit (str): whether hour or day
    """
    packages = Package.objects.filter(
        period__validity_unit=package_validity_unit)
    invoices = {package: [create_subcription_invoice(
        subscription) for subscription in package.package_subscriptions.filter(status=VALIDITY_STATUS_ACTIVE)] for package in packages}
    return invoices
