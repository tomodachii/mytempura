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
        redirect = None

        if hasattr(bot, "elizabot") and bot.elizabot is not None:
            # Redirect to ElizaBot admin change form
            redirect = HttpResponseRedirect(
                reverse("admin:keywordrecognition_elizabot_change", args=[object_id])
            )

        if hasattr(bot, "nlpbot") and bot.nlpbot is not None:
            # Redirect to NLPBot admin change form
            redirect = HttpResponseRedirect(
                reverse("admin:nlp_nlpbot_change", args=[object_id])
            )

        if redirect:
            return redirect
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )


admin_site.register(Bot, BotAdmin)
