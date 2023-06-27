from django.contrib import admin
from main.admin import admin as admin_site
from keywordrecognition.models import Decomp
from django.urls import reverse
from django.utils.html import format_html
from .inline import ReasmbInline


class DecompAdmin(admin.ModelAdmin):
    list_display = ["pattern", "keyword_link"]
    search_fields = ["pattern", "keyword__word"]
    list_filter = ["keyword"]
    list_display_links = ["pattern"]
    inlines = [ReasmbInline]

    def get_queryset(self, request):
        # Get the current logged-in admin user
        queryset = self.model.objects.none()
        owner = request.user

        if owner.selected_bot:
            queryset = (
                super()
                .get_queryset(request)
                .filter(keyword__bot__owner=owner, keyword__bot=owner.selected_bot)
            )

        return queryset

    def keyword_link(self, obj):
        url = reverse("admin:keywordrecognition_keyword_change", args=[obj.keyword.pk])
        return format_html('<a href="{}">{}</a>', url, obj.keyword.word)

    keyword_link.short_description = "keyword"


admin_site.register(Decomp, DecompAdmin)
