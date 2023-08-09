from django.utils.translation import gettext_lazy as _
from .base import ModelBase
from django.db import models


class Response(ModelBase):
    class Meta:
        db_table = "nlp_response"
        ordering = ["pk"]
        verbose_name = _("response")
        verbose_name_plural = _("responses")

    intent = models.ForeignKey(
        "nlp.Intent", on_delete=models.CASCADE, verbose_name=_("intent")
    )

    response = models.CharField(verbose_name=_("response"))

    INSTANT = "INSTANT"
    COLLECT = "COLLECT"
    PROVIDE = "PROVIDE"
    PROVIDE_CONFIRM = "PROVIDE_CONFIRM"
    CONFIRM_POSITIVE_COLLECT = "CONFIRM_POSITIVE_COLLECT"
    CONFIRM_POSITIVE = "CONFIRM_POSITIVE"
    CONFIRM_NEGATIVE = "CONFIRM_NEGATIVE"

    RESPONSE_TYPE = [
        (INSTANT, _("Instant response")),
        (COLLECT, _("Collect response")),
        (PROVIDE, _("Provide response")),
        (PROVIDE_CONFIRM, _("Provide Confirm response")),
        (CONFIRM_POSITIVE_COLLECT, _("Provide Confirm Collect response")),
        (CONFIRM_POSITIVE, _("Positive response")),
        (CONFIRM_NEGATIVE, _("Negative response")),
    ]

    message_type = models.CharField(
        max_length=64,
        choices=RESPONSE_TYPE,
        default=INSTANT,
        verbose_name=_("response type"),
    )

    def __str__(self):
        return self.response
