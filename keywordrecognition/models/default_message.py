from django.db import models
from .base import ModelBase
from django.db.models import Manager
from django.db.models.aggregates import Count
from random import randint
from django.utils.translation import gettext_lazy as _


# Default message for chatbot

class DefaultMessageCustomManager(Manager):
    def random_fallback(self, bot=None):
        if bot:
            count = self.filter(bot=bot, message_type=DefaultMessage.FALLBACK).aggregate(count=Count('id'))['count']
            random_index = randint(0, count - 1)
            return self.filter(bot=bot, message_type=DefaultMessage.FALLBACK)[random_index]
        return None


class DefaultMessage(ModelBase):
    class Meta:
        db_table = 'keywordrecognition_default_message'
        ordering = ['pk']
        verbose_name = _('default message')
        verbose_name_plural = _('default messages')

    bot = models.ForeignKey('keywordrecognition.ElizaBot', on_delete=models.CASCADE, verbose_name=_('bot'))
    message = models.TextField(verbose_name=_('default message'))

    default_message_objects = DefaultMessageCustomManager()

    INITIAL = 'INITIAL'
    FINAL = 'FINAL'
    FALLBACK = 'FALLBACK'

    MESSAGE_TYPE = [
        (INITIAL, 'Initial'),
        (FINAL, 'Final'),
        (FALLBACK, 'Fallback'),
    ]

    message_type = models.CharField(
        max_length=64,
        choices=MESSAGE_TYPE,
        default=FALLBACK,
        verbose_name='default message type'
    )
