from django.utils.translation import gettext_lazy as _
from .base import ModelBase
from django.db import models


class TrainingPhrase(ModelBase):
    class Meta:
        db_table = "nlp_training_phrase"
        ordering = ["pk"]
        verbose_name = _("training phrase")
        verbose_name_plural = _("training phrases")

    intent = models.ForeignKey(
        "nlp.Intent", on_delete=models.CASCADE, verbose_name=_("intent")
    )

    phrase = models.CharField(verbose_name=_("phrase"))

    def __str__(self):
        return self.phrase
