from django.apps import AppConfig


class SubscriptionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscriptions'
    icon = 'fa fa-credit-card-alt'
    
    def ready(self):
        from subscriptions import signals
