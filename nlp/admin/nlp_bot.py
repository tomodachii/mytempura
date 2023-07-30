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

    def intent_count(self, obj):
        return obj.intent_set.count()

    intent_count.short_description = "intent count"


admin_site.register(NLPBot, NLPBotAdmin)
