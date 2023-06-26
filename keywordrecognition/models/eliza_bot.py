from django.utils.translation import gettext_lazy as _
from .default_message import DefaultMessage
from backend.models import Bot


class ElizaBot(Bot):
    class Meta:
        db_table = "keywordrecognition_eliza_bot"
        ordering = ["pk"]
        verbose_name = _("eliza bot")
        verbose_name_plural = _("eliza bots")

    def get_keywords(self):
        return self.keyword_set.all()

    def get_random_initial_message(self):
        initial_messages = self.default_messages.filter(
            message_type=DefaultMessage.INITIAL
        )
        if initial_messages.exists():
            return initial_messages.order_by("?").first().message
        return _("Hello! Please tell me your problem")
