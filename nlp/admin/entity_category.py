from django.contrib import admin
from main.admin import admin as admin_site
from nlp.models import EntityCategory


class EntityCategoryAdmin(admin.ModelAdmin):
    list_display = ["category_name"]

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


admin_site.register(EntityCategory, EntityCategoryAdmin)
