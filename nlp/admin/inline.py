from django.contrib import admin
from nlp.models import TrainingPhrase


class TrainingPhraseInline(admin.TabularInline):
    model = TrainingPhrase
    show_change_link = True
    extra = 0
