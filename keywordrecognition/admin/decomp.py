from django.contrib import admin
from keywordrecognition.models import Decomp
from django.urls import reverse
from django.utils.html import format_html
from .inline import ReasmbInline


class DecompAdmin(admin.ModelAdmin):
    list_display = ["id", "keyword_link", "pattern", "bot_link"]
    search_fields = ["keyword__word", "pattern"]
    list_filter = ["keyword__bot"]
    list_display_links = ["id", "pattern"]
    inlines = [ReasmbInline]

    def keyword_link(self, obj):
        url = reverse("admin:keywordrecognition_keyword_change", args=[obj.keyword.pk])
        return format_html('<a href="{}">{}</a>', url, obj.keyword.word)

    keyword_link.short_description = "keyword"

    def bot_link(self, obj):
        url = reverse(
            "admin:keywordrecognition_elizabot_change", args=[obj.keyword.bot.pk]
        )
        return format_html('<a href="{}">{}</a>', url, obj.keyword.bot)

    bot_link.short_description = "bot"


admin.site.register(Decomp, DecompAdmin)
