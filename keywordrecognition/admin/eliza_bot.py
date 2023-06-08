from django.contrib import admin
from keywordrecognition.models import ElizaBot
from .inline import KeywordInline


class ElizaBotAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "owner", "keyword_count"]
    search_fields = ["name", "owner__email"]
    inlines = [KeywordInline]

    def keyword_count(self, obj):
        return obj.keyword_set.count()

    keyword_count.short_description = "keyword count"


admin.site.register(ElizaBot, ElizaBotAdmin)
