from .base import ModelBase
from django.db import models
from django.utils.translation import gettext_lazy as _


class Bot(ModelBase):
    class Meta:
        db_table = "backend_bot"
        ordering = ["pk"]
        verbose_name = _("bot")
        verbose_name_plural = _("bots")

    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.TextField(null=True, blank=True, verbose_name=_("description"))
    owner = models.ForeignKey(
        "backend.Account", on_delete=models.CASCADE, verbose_name=_("owner")
    )

    def __str__(self):
        return f"{self.owner}'s {self.name}"
