from django.contrib import admin
from main.admin import admin as admin_site
from keywordrecognition.models import Synonym


class SynonymAdmin(admin.ModelAdmin):
    list_display = ["id", "word", "value"]
    search_fields = ["word", "value"]
    list_display_links = ["id"]


admin_site.register(Synonym, SynonymAdmin)
