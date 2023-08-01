from django.utils.translation import gettext_lazy as _
from .base import ModelBase
from django.db import models


class ResponseEntityCategory(ModelBase):
    class Meta:
        db_table = "nlp_response_entity_category"
        ordering = ["response"]
        verbose_name = _("required entity category")
        verbose_name_plural = _("required entity category")

    response = models.ForeignKey(
        "nlp.Response", on_delete=models.CASCADE, verbose_name=_("response")
    )
    required_category = models.ForeignKey(
        "nlp.EntityCategory",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("required entity category"),
    )

    def __str__(self):
        return f"{self.required_category}"
