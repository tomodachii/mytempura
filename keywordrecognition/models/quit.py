from django.db import models
from .base import ModelBase
from django.utils.translation import gettext_lazy as _


# Quit message for chatbot


class Quit(ModelBase):
    class Meta:
        db_table = "keywordrecognition_quit"
        ordering = ["pk"]
        verbose_name = _("quit message")
        verbose_name_plural = _("quit messages")

    bot = models.ForeignKey(
        "keywordrecognition.ElizaBot", on_delete=models.CASCADE, verbose_name=_("bot")
    )
    trigger = models.CharField(max_length=255, verbose_name=_("trigger"))
