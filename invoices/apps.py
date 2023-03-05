from django.apps import AppConfig


class InvoicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'invoices'
    icon = 'fa fa-money'
    
    def ready(self):
        from invoices import signals
