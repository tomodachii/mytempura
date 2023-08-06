from django.contrib import admin as admin_site
from backend.models import Bot
from django.urls import path
from django.http import JsonResponse
from django.conf import settings

# from django.urls import reverse
# from django.shortcuts import redirect


class AdminSite(admin_site.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "update-selected-bot/",
                self.update_selected_bot,
                name="update-selected-bot",
            ),
        ]
        return custom_urls + urls

    def update_selected_bot(self, request):
        bot_id = request.GET.get("selected-bot")
        # Perform necessary logic to update the context based on the selected value
        try:
            account = request.user
            if not bot_id:
                account.selected_bot = None
                account.save()
                return JsonResponse({"message": "Unselected Bot"})
            selected_bot = Bot.objects.get(id=bot_id)
            account.selected_bot = selected_bot
            account.save()

            if hasattr(selected_bot, "elizabot") and selected_bot.elizabot is not None:
                # Redirect to ElizaBot admin change form
                return JsonResponse(
                    {"message": "Selected Bot", "type": "eliza", "bot_id": bot_id}
                )

            if hasattr(selected_bot, "nlpbot") and selected_bot.nlpbot is not None:
                # Redirect to NLPBot admin change form
                return JsonResponse(
                    {"message": "Selected Bot", "type": "nlp", "bot_id": bot_id}
                )
        except Exception as e:
            return JsonResponse({"message": e})

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context["bots_count"] = Bot.objects.filter(owner=request.user).count()
        return super(AdminSite, self).index(request, extra_context)

    def each_context(self, request):
        exclude_app_list = ["api"]
        context = super(AdminSite, self).each_context(request)
        bot_type = ""
        if request.user.is_authenticated:
            bots = Bot.objects.filter(owner=request.user)
            selected_bot = request.user.selected_bot
        else:
            bots = []
            selected_bot = None
        if selected_bot:
            if hasattr(selected_bot, "elizabot"):
                exclude_app_list.append("nlp")
                bot_type = "elizabot"
            elif hasattr(selected_bot, "nlpbot"):
                exclude_app_list.append("keywordrecognition")
                bot_type = "nlpbot"
        else:
            exclude_app_list.append("nlp")
            exclude_app_list.append("keywordrecognition")
        context.update(
            {
                "backend_url": settings.BACKEND_URL,
                "exclude_app_list": exclude_app_list,
                "bots": bots,
                "selected_bot": selected_bot,
                "bot_type": bot_type,
            }
        )
        return context


admin = AdminSite()
