from django.contrib import admin as admin_site
from keywordrecognition.models import ElizaBot


class AdminSite(admin_site.AdminSite):
    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context["eliza_bots_count"] = ElizaBot.objects.filter(
            owner=request.user
        ).count()
        return super(AdminSite, self).index(request, extra_context)

    def each_context(self, request):
        context = super(AdminSite, self).each_context(request)
        context.update(
            {
                "exclude_app_list": ["backend"],
            }
        )
        return context


admin = AdminSite()
