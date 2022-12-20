from django.apps import AppConfig

# from django.utils.translation import gettext_lazy as _


class QuotesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "quotes"
    verbose_name = _("Quotes")
