from invoices.models import Invoice
from subscriptions.models import Subscription, Package
from datetime import datetime
from utils.constants import VALIDITY_STATUS_ACTIVE, VALIDITY_UNIT_DAYS
from invoices.helperMixins import BillingModelMixin
from typing import Any

def create_subcription_invoice(subscription: Subscription, **kwargs)->Any:
    """
    helper function to create a invoice for a subscription
    it takes in count all the different billing model rules

    Args:
        subscription (Subscription): active subscription

    Returns:
        Invoice: created invoice
        OR
        Periodic Task: renewal subscription scheduled
    """
    package_billing_method = BillingModelMixin.model_billing_method(subscription.package.billing_model)
    return package_billing_method(subscription=subscription, **kwargs)

        
