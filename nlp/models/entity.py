from django.utils.translation import gettext_lazy as _
from .base import ModelBase
from django.db import models


class Entity(ModelBase):
    class Meta:
        db_table = "nlp_entity"
        ordering = ["pk"]
        verbose_name = _("entity")
        verbose_name_plural = _("entities")

    bot = models.ForeignKey(
        "nlp.NLPBot", on_delete=models.CASCADE, verbose_name=_("nlp bot")
    )
    entity_name = models.CharField(
        max_length=100, null=False, verbose_name=_("entity name")
    )

    entity_category = models.ForeignKey(
        "nlp.EntityCategory",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("entity category"),
    )

    synonym = models.CharField(null=True, blank=True, verbose_name=_("synonym"))

    def __str__(self):
        return self.entity_name
