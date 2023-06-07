from django.contrib import admin
from keywordrecognition.models import Synonym


class SynonymAdmin(admin.ModelAdmin):
    list_display = ['id', 'word', 'value']
    search_fields = ['word', 'value']
    list_display_links = ['id']


admin.site.register(Synonym, SynonymAdmin)
