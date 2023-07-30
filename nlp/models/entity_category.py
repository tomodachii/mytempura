from django.utils.translation import gettext_lazy as _
from .base import ModelBase
from django.db import models


class EntityCategory(ModelBase):
    class Meta:
        db_table = "nlp_entity_category"
        ordering = ["pk"]
        verbose_name = _("entity category")
        verbose_name_plural = _("entity categories")

    bot = models.ForeignKey(
        "nlp.NLPBot", on_delete=models.CASCADE, verbose_name=_("nlp bot")
    )
    category_name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.category_name
