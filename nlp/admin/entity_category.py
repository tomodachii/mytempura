from django.contrib import admin
from main.admin import admin as admin_site
from nlp.models import EntityCategory


class EntityCategoryAdmin(admin.ModelAdmin):
    pass


admin_site.register(EntityCategory, EntityCategoryAdmin)
