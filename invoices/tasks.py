from subscription_service import celery_app
from utils.helpers import create_subcription_invoice
from subscriptions.models import Subscription
from datetime import datetime
from typing import Union


@celery_app.task
def invoice_subscription_task(subscription: Union[Subscription, int]):
    """
    celery task for invoicing a subscription

    Args:
        subscription (Subscription): active subscription

    Returns:
        None
    """
    if isinstance(subscription, int):
        subscription = Subscription.objects.get(id=subscription)

    return create_subcription_invoice(subscription)


@celery_app.task
def renew_subscription(subscription:Union[Subscription,int]):
    if isinstance(subscription, int):
        subscription = Subscription.objects.get(id=subscription)
        
    #run invoicing
    subscription.current_invoicing_end_date = None
    return create_subcription_invoice(subscription)