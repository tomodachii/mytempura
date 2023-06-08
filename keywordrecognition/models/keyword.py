from django.db import models
from .base import ModelBase
from django.utils.translation import gettext_lazy as _


class Keyword(ModelBase):
    class Meta:
        db_table = "keywordrecognition_keyword"
        ordering = ["-weight"]
        verbose_name = _("keyword")
        verbose_name_plural = _("keywords")

    bot = models.ForeignKey(
        "keywordrecognition.ElizaBot", on_delete=models.CASCADE, verbose_name=_("bot")
    )
    word = models.CharField(max_length=255, verbose_name=_("word"))
    weight = models.IntegerField(default=1, verbose_name=_("weight"))

    def __str__(self):
        return self.word
