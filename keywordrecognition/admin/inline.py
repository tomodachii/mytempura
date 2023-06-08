from django.contrib import admin
from keywordrecognition.models import Keyword, Decomp, Reasmb


class KeywordInline(admin.TabularInline):
    model = Keyword
    show_change_link = True
    extra = 0


class DecompInline(admin.TabularInline):
    model = Decomp
    show_change_link = True
    extra = 0


class ReasmbInline(admin.TabularInline):
    model = Reasmb
    show_change_link = True
    extra = 0
