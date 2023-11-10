from django.contrib import admin

from .models import School

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    search_fields = ["code", "name"]
    list_display = ["name", "district", "code"]
    autocomplete_fields = ["district"]
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "code", "owner", "email", "gender", "telephone")},
        ),
        (
            "Location Information",
            {"fields": ("district", "town", "digital_address", "location")},
        ),
        (
            "Other Information",
            {
                "fields": ("description", "date_established", "logo", "visible"),
            },
        ),
    )
