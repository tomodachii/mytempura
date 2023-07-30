from django.utils.translation import gettext_lazy as _
from .base import ModelBase
from django.db import models


class ResponseEntity(ModelBase):
    class Meta:
        db_table = "nlp_response_entity"
        ordering = ["response"]
        verbose_name = _("response entity mapping")
        verbose_name_plural = _("response entity mapping")

    response = models.ForeignKey(
        "nlp.Response", on_delete=models.CASCADE, verbose_name=_("response")
    )
    entity = models.ForeignKey(
        "nlp.Entity", on_delete=models.CASCADE, verbose_name=_("entity")
    )

    def __str__(self):
        return f"{self.entity}"
