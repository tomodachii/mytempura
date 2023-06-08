from django.contrib import admin
from keywordrecognition.models import PostProcessing


class PostProcessingAdmin(admin.ModelAdmin):
    list_display = ["id", "input_word", "output_word"]
    search_fields = ["input_word", "output_word"]
    list_display_links = ["id"]


admin.site.register(PostProcessing, PostProcessingAdmin)
