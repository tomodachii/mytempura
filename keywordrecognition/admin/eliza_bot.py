from django.contrib import admin
from main.admin import admin as admin_site
from keywordrecognition.models import ElizaBot
from .inline import KeywordInline
from django.template.response import TemplateResponse
from django.urls import path
from django.conf import settings


class ElizaBotAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "owner", "keyword_count"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "owner__email"]
    inlines = [KeywordInline]
    change_form_template = "admin/eliza_bot/elizabot_change_form.html"

    def get_queryset(self, request):
        queryset = self.model.objects.none()
        # Get the current logged-in admin user
        owner = request.user

        # Filter the queryset to only include items belonging to the admin user
        queryset = super().get_queryset(request).filter(owner=owner)

        return queryset

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/test/",
                self.admin_site.admin_view(self.test_bot_view),
                name="elizabot-test-bot",
            ),
        ]
        return custom_urls + urls

    def test_bot_view(self, request, object_id):
        # Retrieve the ElizaBot instance
        elizabot = self.get_object(request, object_id)
        context = self.admin_site.each_context(request)
        context["elizabot"] = elizabot
        context["backend_url"] = settings.BACKEND_URL

        # input = request.POST.get("input")
        # # Handle form submission
        # if request.method == 'POST':
        #     response = self.test_bot(elizabot)
        #     context['response'] = response

        template = "admin/eliza_bot/elizabot_test.html"
        return TemplateResponse(request, template, context)

    def keyword_count(self, obj):
        return obj.keyword_set.count()

    keyword_count.short_description = "keyword count"


admin_site.register(ElizaBot, ElizaBotAdmin)
