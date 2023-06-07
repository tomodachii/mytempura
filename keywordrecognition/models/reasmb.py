from django.db import models
from .base import ModelBase
from django.utils.translation import gettext_lazy as _


# Reassembling Rules


class Reasmb(ModelBase):
    class Meta:
        db_table = 'keywordrecognition_reasmb'
        ordering = ['pk']
        verbose_name = _('reassembling rule')
        verbose_name_plural = _('reassembling rules')

    decomp = models.ForeignKey('keywordrecognition.Decomp', on_delete=models.CASCADE, verbose_name=_('decomp'))
    template = models.TextField(verbose_name=_('template'))

    def get_reasmb_template_words(self) -> list[str]:
        return self.template.split()
