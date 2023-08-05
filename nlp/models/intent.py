from django.utils.translation import gettext_lazy as _
from .base import ModelBase
from django.db import models


class Intent(ModelBase):
    class Meta:
        db_table = "nlp_intent"
        ordering = ["pk"]
        verbose_name = _("intent")
        verbose_name_plural = _("intents")

    bot = models.ForeignKey(
        "nlp.NLPBot", on_delete=models.CASCADE, verbose_name=_("nlp bot")
    )
    intent_name = models.CharField(
        max_length=100, null=False, verbose_name=_("intent name")
    )

    def __str__(self):
        return self.intent_name
