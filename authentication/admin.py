from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from authentication.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ["email", "name"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]

    list_display = [
        "email",
        "name",
        "is_active",
        "is_admin",
        "created_at",
    ]

    list_filter = [
        "is_active",
        "is_admin",
        "created_at",
    ]

    filter_horizontal = []
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    add_fieldsets = (
        (
            _("Details"),
            {
                "fields": [
                    "email",
                    "name",
                    "bio",
                ]
            },
        ),
        (
            _("Access"),
            {"fields": ["is_active", "is_admin"]},
        ),
    )

    fieldsets = (
        (
            _("Details"),
            {
                "fields": [
                    "id",
                    "uuid",
                    "email",
                    "name",
                    "bio",
                ]
            },
        ),
        (
            _("Access"),
            {
                "fields": [
                    "is_active",
                    "is_admin",
                    "password",
                    "verification_token",
                ]
            },
        ),
        (_("Dates"), {"fields": ["created_at", "updated_at"]}),
    )

    def save_model(self, request, obj, form, change):
        """Override save_model to ensure UserManager is used for saving."""
        obj.full_clean()  # Ensure model validation
        obj.save(using=self._db)

    class Media:
        pass
