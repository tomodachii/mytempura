from django.db import models
from .base import ModelBase
from django.utils.translation import gettext_lazy as _


class PostProcessing(ModelBase):
    class Meta:
        db_table = "keywordrecognition_postprocessing"
        ordering = ["input_word"]
        verbose_name = _("post processing")
        verbose_name_plural = _("post processing")

    input_word = models.CharField(max_length=255, verbose_name=_("input word"))
    output_word = models.CharField(max_length=255, verbose_name=_("output word"))
