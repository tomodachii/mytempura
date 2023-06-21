from django.contrib import admin
from main.admin import admin as admin_site
from keywordrecognition.models import DefaultMessage
from django.urls import reverse
from django.utils.html import format_html


class DefaultMessageAdmin(admin.ModelAdmin):
    list_display = ["id", "bot_link", "message", "message_type"]
    search_fields = ["message", "bot__name"]
    list_filter = ["message_type"]
    list_display_links = ["id", "message"]

    def get_queryset(self, request):
        # Get the current logged-in admin user
        owner = request.user

        # Filter the queryset to only include items belonging to the admin user
        queryset = super().get_queryset(request).filter(bot__owner=owner)

        return queryset

    def bot_link(self, obj):
        url = reverse("admin:keywordrecognition_elizabot_change", args=[obj.bot.pk])
        return format_html('<a href="{}">{}</a>', url, obj.bot)

    bot_link.short_description = "bot"


admin_site.register(DefaultMessage, DefaultMessageAdmin)
