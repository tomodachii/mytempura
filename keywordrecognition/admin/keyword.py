from django.contrib import admin
from main.admin import admin as admin_site
from keywordrecognition.models import Keyword
from .inline import DecompInline


class KeywordAdmin(admin.ModelAdmin):
    list_display = ["word", "weight"]
    search_fields = ["word"]
    list_filter = ["weight"]
    list_display_links = ["word"]
    inlines = [DecompInline]

    def get_queryset(self, request):
        # Get the current logged-in admin user
        queryset = self.model.objects.none()
        owner = request.user

        if owner.selected_bot:
            queryset = (
                super()
                .get_queryset(request)
                .filter(bot__owner=owner, bot=owner.selected_bot)
            )

        return queryset


admin_site.register(Keyword, KeywordAdmin)
