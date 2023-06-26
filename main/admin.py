from django.contrib import admin as admin_site
from backend.models import Bot
from django.urls import path
from django.http import JsonResponse


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
            return JsonResponse({"message": "Select Bot"})
        except Exception as e:
            return JsonResponse({"message": e})

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context["bots_count"] = Bot.objects.filter(owner=request.user).count()
        return super(AdminSite, self).index(request, extra_context)

    def each_context(self, request):
        context = super(AdminSite, self).each_context(request)
        if request.user.is_authenticated:
            bots = Bot.objects.filter(owner=request.user)
            selected_bot = request.user.selected_bot
        else:
            bots = []
            selected_bot = None
        context.update(
            {
                "exclude_app_list": ["api"],
                "bots": bots,
                "selected_bot": selected_bot,
            }
        )
        return context


admin = AdminSite()
