from django.contrib import admin
from keywordrecognition.models import DefaultMessage
from django.urls import reverse
from django.utils.html import format_html


class DefaultMessageAdmin(admin.ModelAdmin):
    list_display = ["id", "bot_link", "message", "message_type"]
    search_fields = ["message", "bot__name"]
    list_filter = ["message_type"]
    list_display_links = ["id", "message"]

    def bot_link(self, obj):
        url = reverse("admin:keywordrecognition_elizabot_change", args=[obj.bot.pk])
        return format_html('<a href="{}">{}</a>', url, obj.bot)

    bot_link.short_description = "bot"


admin.site.register(DefaultMessage, DefaultMessageAdmin)
