from django.contrib import admin
from main.admin import admin as admin_site
from keywordrecognition.models import PostProcessing


class PostProcessingAdmin(admin.ModelAdmin):
    list_display = ["id", "input_word", "output_word"]
    search_fields = ["input_word", "output_word"]
    list_display_links = ["id"]


admin_site.register(PostProcessing, PostProcessingAdmin)
