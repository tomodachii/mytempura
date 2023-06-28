from django.db import models
from .base import ModelBase
import random
from django.utils.translation import gettext_lazy as _

# Decomposition Rule


class Decomp(ModelBase):
    class Meta:
        db_table = "keywordrecognition_decomp"
        ordering = ["pk"]
        verbose_name = _("decomposition rule")
        verbose_name_plural = _("decomposition rules")

    keyword = models.ForeignKey(
        "keywordrecognition.Keyword",
        on_delete=models.CASCADE,
        verbose_name=_("keyword"),
    )
    pattern = models.CharField(max_length=255, verbose_name=_("pattern"))
    weight = models.IntegerField(default=1, verbose_name=_("weight"))

    def __str__(self):
        return f"{self.pattern}"

    def get_random_reasmb(self):
        reasmb_set = self.reasmb_set.all()
        if not reasmb_set:
            return None
        return random.choice(reasmb_set)

    def get_decomp_pattern_parts(self) -> list[str]:
        pattern_words = self.pattern.split(" ")
        output = []
        phrase = ""
        for word in pattern_words:
            if word == "*":
                if phrase:
                    output.append(phrase.strip())
                    phrase = ""
                output.append(word)
            else:
                phrase = " ".join([phrase, word])
        if phrase:
            output.append(phrase.strip())
        return output
