from django.contrib import admin
from main.admin import admin as admin_site
from nlp.models import NLPBot

# from django.template.response import TemplateResponse
# from django.urls import path
# from django.conf import settings


class NLPBotAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "owner", "intent_count"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "owner__email"]

    def get_queryset(self, request):
        queryset = self.model.objects.none()
        # Get the current logged-in admin user
        owner = request.user

        # Filter the queryset to only include items belonging to the admin user
        queryset = super().get_queryset(request).filter(owner=owner)

        return queryset

    # Set selected bot in context
    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        nlpbot = self.get_object(request, object_id)
        context = self.admin_site.each_context(request)
        context["selected_bot"] = nlpbot
        user = request.user
        user.selected_bot = nlpbot
        user.save()
        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )

    def intent_count(self, obj):
        return obj.intent_set.count()

    intent_count.short_description = "intent count"


admin_site.register(NLPBot, NLPBotAdmin)
