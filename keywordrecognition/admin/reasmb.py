from django.contrib import admin
from main.admin import admin as admin_site
from keywordrecognition.models import Reasmb
from django.urls import reverse
from django.utils.html import format_html


class ReasmbAdmin(admin.ModelAdmin):
    list_display = ["template", "decomp_link", "keyword_link"]
    search_fields = [
        "decomp__pattern",
        "template",
        "decomp__keyword__word",
    ]
    list_display_links = ["template"]

    def get_queryset(self, request):
        # Get the current logged-in admin user
        queryset = self.model.objects.none()
        owner = request.user

        if owner.selected_bot:
            queryset = (
                super()
                .get_queryset(request)
                .filter(
                    decomp__keyword__bot__owner=owner,
                    decomp__keyword__bot=owner.selected_bot,
                )
            )

        return queryset

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
