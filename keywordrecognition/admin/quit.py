from django.contrib import admin
from keywordrecognition.models import Quit
from django.urls import reverse
from django.utils.html import format_html


class QuitAdmin(admin.ModelAdmin):
    list_display = ["id", "bot_link", "trigger"]
    search_fields = ["trigger", "bot__name"]
    list_display_links = ["id", "trigger"]

    def bot_link(self, obj):
        url = reverse("admin:keywordrecognition_elizabot_change", args=[obj.bot.pk])
        return format_html('<a href="{}">{}</a>', url, obj.bot)

    bot_link.short_description = "bot"


admin.site.register(Quit, QuitAdmin)
