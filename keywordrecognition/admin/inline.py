from django.contrib import admin
from keywordrecognition.models import Keyword, Decomp, Reasmb


class KeywordInline(admin.StackedInline):
    model = Keyword
    show_change_link = True
    extra = 0


class DecompInline(admin.StackedInline):
    model = Decomp
    show_change_link = True
    extra = 0


class ReasmbInline(admin.StackedInline):
    model = Reasmb
    show_change_link = True
    extra = 0
