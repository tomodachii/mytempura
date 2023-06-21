from django.contrib import admin
from main.admin import admin as admin_site
from keywordrecognition.models import Reasmb
from django.urls import reverse
from django.utils.html import format_html


class ReasmbAdmin(admin.ModelAdmin):
    list_display = ["id", "bot_link", "keyword_link", "decomp_link", "template"]
    search_fields = [
        "decomp__pattern",
        "template",
        "decomp__keyword__word",
        "decomp__keyword__bot__name",
    ]
    list_display_links = ["id", "template"]

    def get_queryset(self, request):
        # Get the current logged-in admin user
        owner = request.user

        # Filter the queryset to only include items belonging to the admin user
        queryset = (
            super().get_queryset(request).filter(decomp__keyword__bot__owner=owner)
        )

        return queryset

    def bot_link(self, obj):
        url = reverse(
            "admin:keywordrecognition_elizabot_change", args=[obj.decomp.keyword.bot.pk]
        )
        return format_html('<a href="{}">{}</a>', url, obj.decomp.keyword.bot)

    bot_link.short_description = "bot"

    def keyword_link(self, obj):
        url = reverse(
            "admin:keywordrecognition_keyword_change", args=[obj.decomp.keyword.pk]
        )
        return format_html('<a href="{}">{}</a>', url, obj.decomp.keyword.word)

    keyword_link.short_description = "keyword"

    def decomp_link(self, obj):
        url = reverse("admin:keywordrecognition_decomp_change", args=[obj.decomp.pk])
        return format_html('<a href="{}">{}</a>', url, obj.decomp)

    decomp_link.short_description = "decomp"


admin_site.register(Reasmb, ReasmbAdmin)
