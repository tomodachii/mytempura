from django.contrib import admin
from main.admin import admin as admin_site
from nlp.models import Intent
from .inline import TrainingPhraseInline


class IntentAdmin(admin.ModelAdmin):
    list_display = ["intent_name", "training_phrase_count"]
    search_fields = ["intent_name"]
    list_display_links = ["intent_name"]
    inlines = [TrainingPhraseInline]

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

    def training_phrase_count(self, obj):
        return obj.trainingphrase_set.count()

    training_phrase_count.short_description = "number of training phrases"


admin_site.register(Intent, IntentAdmin)
