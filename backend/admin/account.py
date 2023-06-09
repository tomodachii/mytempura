from django.contrib import admin
from backend.models import Account
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


class AccountAdmin(UserAdmin):
    # search_fields = ["email", "uid"]
    list_display = ["username", "email", "name", "is_active", "last_login"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(Account, AccountAdmin)
