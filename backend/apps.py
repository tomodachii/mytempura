from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BackendConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend"
    verbose_name = _("Account Management")
