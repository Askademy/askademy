from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, UserSchool, PasswordResetRequest
from chat.models import ChatMessage


class UserSchoolInline(admin.StackedInline):
    model = UserSchool
    extra = 1

# admin.site.register(PasswordResetRequest)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [UserSchoolInline]
    ordering = ("id",)
    list_display = ("name", "phone_number")
    readonly_fields = ("school", "last_login", "date_joined")
    search_fields = ("first_name", "middle_name", "last_name", "phone_number")
    list_filter = ("last_login", "date_joined", "is_active", "is_superuser", "is_staff")
    fieldsets = (
        (None, {"fields": ("phone_number", "nickname")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "email",
                    "gender",
                    "bio",
                )
            },
        ),
        (
            "School Info",
            {"fields": ("subjects", "level", "school")},
        ),
        ("Photos", {"fields": ["profile_picture", "cover_picture"]}),
        ("Important Dates", {"fields": ("birthdate", "last_login", "date_joined")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "first_name",
                    "middle_name",
                    "last_name",
                    "birthdate",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    @admin.display()
    def school(self, user):
        """Return the current school of the user"""
        user_school = user.get_current_school()
        if user_school:
            return user_school.school.name
        return "-"

    @admin.display()
    def name(self, user):
        """Return the user full name"""
        return user.get_full_name()

admin.site.register(ChatMessage)