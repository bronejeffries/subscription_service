from datetime import timedelta, datetime as DT
from django.utils import timezone
from typing import Optional, Any, Union
from invoices.models import Invoice
import json
from subscriptions.models import Company
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from utils.constants import (BILLING_MODEL_FEATURE_BASED,
                             BILLING_MODEL_FLAT_RATE, BILLING_MODEL_FREEMIUM,
                             BILLING_MODEL_PAU, BILLING_MODEL_PAYG,
                             BILLING_MODEL_PER_USER,
                             BILLING_MODEL_PER_USER_TIERS,
                             BILLING_MODEL_STORAGE_TIERS,
                             INVOICE_TYPE_SUBSCRIPTION, VALIDITY_UNIT_DAYS,
                             VALIDITY_STATUS_EXPIRED, VALIDITY_STATUS_ACTIVE,
                             VALIDITY_STATUS_PENDING)


class BillingModelMixin(object):

    # all methods listed here must be class methods to this class
    billing_methods_dict = {
        BILLING_MODEL_FEATURE_BASED: "feature",
        BILLING_MODEL_FLAT_RATE: "flat_rate",
        BILLING_MODEL_FREEMIUM: "free",
        BILLING_MODEL_PAU: BILLING_MODEL_PAU,
        BILLING_MODEL_PER_USER_TIERS: BILLING_MODEL_PER_USER_TIERS,
        BILLING_MODEL_STORAGE_TIERS: "storage"
    }

    @classmethod
    def package_billing_dates(cls, package, start_date: Optional[DT] = None) -> tuple:
        """
            calculates the billing dates for a package from the start date

        Args:
            package (Package): Mandatory
            start_date: Optional

        Returns:
            a tuple with start and end dates: (start_date, end_date)
        """
        package_period = package.period
        effective_date = start_date or timezone.now()
        # effective_date = effective_date.replace(minute=0,second=0,microsecond=0)
        time_delta = timedelta(days=package_period.validity_span) if package_period.validity_unit == VALIDITY_UNIT_DAYS else timedelta(
            hours=package_period.validity_span)
        end_date = effective_date + time_delta
        return effective_date, end_date

    @classmethod
    def model_billing_method(cls, billing_model):
        return getattr(cls,
                       "{}_billing".format(
                           cls.billing_methods_dict.get(billing_model)),
                       cls.billing_method_not_implemented
                       )

    @classmethod
    def billing_method_not_implemented(cls, *args, **kwargs):
        raise NotImplemented("Billing model method is not available")

    @classmethod
    def feature_billing(cls, **kwargs) -> Union[Invoice, PeriodicTask]:
        """
         billing method for feature based billing model.
         generates an invoice for a subscription at the start of the billing period
         with a validity span of the package period

         Args:
            subscription (Subscription): subscription instance being invoiced

        Returns:
           A generated invoice if any else None

        """
        return cls.flat_rate_billing(subscription, **kwargs)
    
    @classmethod
    def storage_billing(cls, **kwargs) -> Union[Invoice, PeriodicTask]:
        """
         billing method for storage tiers billing model.
         generates an invoice for a subscription at the start of the billing period
         with a validity span of the package period

         Args:
            subscription (Subscription): subscription instance being invoiced

        Returns:
           A generated invoice if any else None

        """
        return cls.flat_rate_billing(subscription, **kwargs)

    @classmethod
    def flat_rate_billing(cls, subscription, **kwargs) -> Union[Invoice, PeriodicTask]:
        """
         billing method for flat rate billing model.
         generates an invoice for a subscription at the start of the billing period
         with a validity span of the package period

         Args:
            subscription (Subscription): subscription instance being invoiced

        Returns:
           A generated invoice if any else None

        """
        current_invoicing_end: DT = subscription.current_invoicing_end_date
        create_future_invoice = False

        # renew subscription
        if kwargs.get('renew', False) and current_invoicing_end:
            if current_invoicing_end < timezone.now():
                subscription.status = VALIDITY_STATUS_PENDING
                current_invoicing_end = None
            else:
                create_future_invoice = True

        if current_invoicing_end and current_invoicing_end <= timezone.now():
            subscription.status = VALIDITY_STATUS_EXPIRED
            subscription.save()

        # handle invoicing
        if subscription.status == VALIDITY_STATUS_PENDING or create_future_invoice:

            # set billing dates
            effective_date, end_date = cls.package_billing_dates(
                subscription.package, current_invoicing_end)
            subscription.current_invoicing_start_date = effective_date
            subscription.current_invoicing_end_date = end_date
            subscription.save()

            # create invoice
            return Invoice.objects.create(type=INVOICE_TYPE_SUBSCRIPTION,
                                          content_object=subscription,
                                          owner=subscription.owning_entity(),
                                          effective_date=effective_date,
                                          end_date=end_date,
                                          redirect_url=subscription.redirect_url,
                                          amount=subscription.package.rate)

    @classmethod
    def free_billing(cls, subscription, **kwargs) -> Union[Invoice, PeriodicTask]:
        """
        billing method for freemium billing model
        generates an invoice for a subscription at the start of the billing period
        with a validity span of the package period
        marks the invoice as paid

        Args:
            subscription (Subscription): subscription model instance to be invoiced

        Returns:
            generated invoice if any otherwise None
        """
        invoice = cls.flat_rate_billing(subscription, **kwargs)
        if invoice and isinstance(invoice, Invoice):
            invoice.paid = True
            invoice.save()
        return invoice

    @classmethod
    def per_user_tier_billing(cls, subscription, **kwargs) -> Union[Invoice, PeriodicTask]:
        """
         billing method for per user tier billing model.
         generates an invoice for a subscription at the start of the billing period
         with a validity span of the package period

         Args:
            subscription (Subscription): subscription instance being invoiced

        Returns:
           A generated invoice if any else None

        """
        return cls.flat_rate_billing(subscription, **kwargs)

    @classmethod
    def per_active_user_billing(cls, subscription, **kwargs) -> Union[Invoice, PeriodicTask]:
        """
        billing method for the per active user billing model
        sets the current invoicing dates
        generates an invoice at the end of the billing period

        Args:
            subscription (Subscription): subscription to be invoiced
               assumption -> subscription is of status active or pending

        Returns:
            Invoice: generated if invoice if any otherwise None
        """
        invoice = None
        current_invoicing_end: DT = subscription.current_invoicing_end_date

        # renew subscription
        if kwargs.get('renew', False) and current_invoicing_end:
            if current_invoicing_end < timezone.now():
                # reset current invoicing_date to renew now
                current_invoicing_end = None
            else:
                # schedule renew task
                scheduler = CrontabSchedule.objects.get_or_create(minute=current_invoicing_end.minute, hour=current_invoicing_end.hour,
                                                                  day_of_week=current_invoicing_end.weekday(), day_of_month=current_invoicing_end.day,
                                                                  month_of_year=current_invoicing_end.month)
                task = PeriodicTask.objects.create(crontab=scheduler,
                                                   name="Renewing Subscription",
                                                   task="invoices.tasks.renew_subscription",
                                                   args=json.dumps(
                                                       [subscription.id]),
                                                   expires=(
                                                       current_invoicing_end + timedelta(minutes=1)),
                                                   one_off=True)

        # invoice subscription
        if not current_invoicing_end:
            """
                set invoicing dates and status
            """
            current_invoicing_start, current_invoicing_end = cls.package_billing_dates(
                subscription.package)
            subscription.current_invoicing_start_date = current_invoicing_start
            subscription.current_invoicing_end_date = current_invoicing_end
            subscription.status = VALIDITY_STATUS_ACTIVE
            subscription.save()

        if subscription.current_invoicing_end_date <= timezone.now():
            # update subscription status
            subscription.status = VALIDITY_STATUS_EXPIRED
            #  create end of period invoice
            owning_entity = subscription.owning_entity()
            active_clients = 1
            if isinstance(owning_entity, Company):
                # get active clients for a company at the time of billing
                active_clients = owning_entity.company_clients.filter(
                    is_active=True).count()

            billing_amount = (subscription.package.rate*active_clients)

            invoice = Invoice.objects.create(type=INVOICE_TYPE_SUBSCRIPTION,
                                             content_object=subscription,
                                             owner=subscription.owning_entity(),
                                             effective_date=subscription.current_invoicing_start_date,
                                             end_date=subscription.current_invoicing_end_date,
                                             redirect_url=subscription.redirect_url,
                                             amount=billing_amount)
        subscription.save()
        return invoice
