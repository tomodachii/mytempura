from django.contrib import admin
from keywordrecognition.models import Keyword
from django.urls import reverse
from django.utils.html import format_html
from .inline import DecompInline


class KeywordAdmin(admin.ModelAdmin):
    list_display = ["word", "bot_link", "weight"]
    search_fields = ["word"]
    list_filter = ["weight"]
    list_display_links = ["word"]
    inlines = [DecompInline]

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


admin.site.register(Keyword, KeywordAdmin)
