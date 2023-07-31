from django.contrib import admin
from main.admin import admin as admin_site
from nlp.models import Entity
from django.urls import reverse
from django.utils.html import format_html


class EntityAdmin(admin.ModelAdmin):
    list_display = ["entity_name", "entity_category_link"]
    search_fields = ["bot", "entity_name"]
    list_filter = ["entity_category"]
    list_display_links = ["entity_name"]

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

    def entity_category_link(self, obj):
        url = reverse("admin:nlp_entitycategory_change", args=[obj.entity_category.pk])
        return format_html(
            '<a href="{}">{}</a>', url, obj.entity_category.category_name
        )

    entity_category_link.short_description = "entity_category"


admin_site.register(Entity, EntityAdmin)
