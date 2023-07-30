from django.contrib import admin
from main.admin import admin as admin_site
from nlp.models import Response


class ResponseAdmin(admin.ModelAdmin):
    list_display = ["intent", "response", "message_type"]
    search_fields = ["intent", "response"]
    list_display_links = ["intent", "response"]

    def get_queryset(self, request):
        # Get the current logged-in admin user
        queryset = self.model.objects.none()
        owner = request.user

        if owner.selected_bot:
            queryset = (
                super()
                .get_queryset(request)
                .filter(intent__bot__owner=owner, intent__bot=owner.selected_bot)
            )

        return queryset


admin_site.register(Response, ResponseAdmin)
