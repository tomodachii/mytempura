from .base import ModelBase
from django.db import models
from django.utils.translation import gettext_lazy as _
from .default_message import DefaultMessage


class ElizaBot(ModelBase):
    class Meta:
        db_table = "keywordrecognition_eliza_bot"
        ordering = ["pk"]
        verbose_name = _("eliza bot")
        verbose_name_plural = _("eliza bots")

    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.TextField(null=True, blank=True, verbose_name=_("description"))
    owner = models.ForeignKey(
        "backend.Account", on_delete=models.CASCADE, verbose_name=_("owner")
    )

    def __str__(self):
        return f"{self.owner}'s {self.name}"

    def get_keywords(self):
        return self.keyword_set.all()

    def get_random_initial_message(self):
        initial_messages = self.default_messages.filter(
            message_type=DefaultMessage.INITIAL
        )
        if initial_messages.exists():
            return initial_messages.order_by("?").first().message
        return _("Hello! Please tell me your problem")
