from django.contrib import admin
from main.admin import admin as admin_site
from nlp.models import Response
from .inline import ResponseEntityInline, ResponseEntityCategoryInline


class ResponseAdmin(admin.ModelAdmin):
    list_display = ["intent", "response", "message_type"]
    search_fields = ["intent", "response"]
    list_display_links = ["intent", "response"]

    inlines = [ResponseEntityInline, ResponseEntityCategoryInline]
    change_list_template = "admin/response/change_list.html"

    def get_queryset(self, request):
        # Get the current logged-in admin user
        queryset = self.model.objects.none()
        owner = request.user

        if owner.selected_bot:
            queryset = (
                super()
                .get_queryset(request)
                .filter(intent__bot__owner=owner, intent__bot=owner.selected_bot)
            )

        return queryset

    INLINE_MAPPING = {
        Response.COLLECT: [ResponseEntityCategoryInline],
        Response.PROVIDE: [ResponseEntityCategoryInline, ResponseEntityInline],
        Response.PROVIDE_CONFIRM: [ResponseEntityCategoryInline, ResponseEntityInline],
        Response.CONFIRM_POSITIVE_COLLECT: [
            ResponseEntityCategoryInline,
            ResponseEntityInline,
        ],
        Response.CONFIRM_POSITIVE: [ResponseEntityCategoryInline],
    }

    def get_inline_instances(self, request, obj=None):
        inlines = [ResponseEntityCategoryInline, ResponseEntityInline]
        if obj:
            inlines = self.INLINE_MAPPING.get(obj.message_type, [])
        inline_instances = []

        for inline_class in inlines:
            inline = inline_class(self.model, self.admin_site)
            # if request:
            #     if not (obj and inline.has_add_permission(request, obj)):
            #         continue
            #     if not inline.has_change_permission(request, obj):
            #         continue
            #     if not inline.has_delete_permission(request, obj):
            #         continue
            #     if not inline.has_view_or_change_permission(request, obj):
            #         continue
            #     if not inline.has_view_permission(request, obj):
            #         continue

            inline_instances.append(inline)

        return inline_instances


admin_site.register(Response, ResponseAdmin)
