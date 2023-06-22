from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KeywordrecognitionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "keywordrecognition"
    verbose_name = _("Keyword Chatbot")
