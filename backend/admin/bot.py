from django.contrib import admin
from main.admin import admin as admin_site
from backend.models import Bot
from django.urls import reverse
from django.http import HttpResponseRedirect


class BotAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "owner"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "owner__email"]

    def get_queryset(self, request):
        queryset = self.model.objects.none()
        # Get the current logged-in admin user
        owner = request.user

        # Filter the queryset to only include items belonging to the admin user
        queryset = super().get_queryset(request).filter(owner=owner)

        return queryset

    def change_view(self, request, object_id, form_url="", extra_context=None):
        bot = self.get_object(request, object_id)

        if hasattr(bot, "elizabot") and bot.elizabot is not None:
            # Redirect to ElizaBot admin change form
            return HttpResponseRedirect(
                reverse("admin:keywordrecognition_elizabot_change", args=[object_id])
            )


admin_site.register(Bot, BotAdmin)
