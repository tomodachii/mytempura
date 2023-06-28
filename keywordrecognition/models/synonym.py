from django.db import models
from .base import ModelBase
from django.utils.translation import gettext_lazy as _


class Synonym(ModelBase):
    class Meta:
        db_table = "keywordrecognition_synonym"
        ordering = ["value"]
        verbose_name = _("synonym")
        verbose_name_plural = _("synonyms")

    bot = models.ForeignKey(
        "keywordrecognition.ElizaBot",
        on_delete=models.CASCADE,
        verbose_name=_("bot"),
    )
    word = models.CharField(max_length=255, verbose_name=_("word"))
    value = models.CharField(max_length=255, verbose_name=_("value"))

    def __str__(self):
        return self.word
