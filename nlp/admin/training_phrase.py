from django.contrib import admin
from main.admin import admin as admin_site
from nlp.models import TrainingPhrase


class TrainingPhraseAdmin(admin.ModelAdmin):
    list_display = ["intent", "phrase"]
    search_fields = ["intent", "phrase"]
    list_display_links = ["intent", "phrase"]

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


admin_site.register(TrainingPhrase, TrainingPhraseAdmin)
