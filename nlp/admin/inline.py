from django.contrib import admin
from nlp.models import TrainingPhrase, ResponseEntity, ResponseEntityCategory


class TrainingPhraseInline(admin.TabularInline):
    model = TrainingPhrase
    show_change_link = True
    extra = 0


class ResponseEntityInline(admin.TabularInline):
    model = ResponseEntity
    show_change_link = True
    extra = 0


class ResponseEntityCategoryInline(admin.TabularInline):
    model = ResponseEntityCategory
    show_change_link = True
    extra = 0
