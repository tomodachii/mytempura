from django.contrib import admin
from main.admin import admin as admin_site
from keywordrecognition.models import DefaultMessage


class DefaultMessageAdmin(admin.ModelAdmin):
    list_display = ["message", "message_type"]
    search_fields = ["message"]
    list_filter = ["message_type"]
    list_display_links = ["message"]

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


admin_site.register(DefaultMessage, DefaultMessageAdmin)
