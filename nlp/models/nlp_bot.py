from django.utils.translation import gettext_lazy as _
from backend.models import Bot


class NLPBot(Bot):
    class Meta:
        db_table = "nlp_bot"
        ordering = ["pk"]
        verbose_name = _("nlp bot")
        verbose_name_plural = _("nlp bots")
