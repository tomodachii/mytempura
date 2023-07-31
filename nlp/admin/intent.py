from django.contrib import admin
from main.admin import admin as admin_site
from nlp.models import Intent


class IntentAdmin(admin.ModelAdmin):
    list_display = ["intent_name"]
    search_fields = ["bot", "intent_name"]
    list_display_links = ["intent_name"]

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


admin_site.register(Intent, IntentAdmin)
