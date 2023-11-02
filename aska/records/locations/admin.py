from django.contrib import admin

from .models import District, Region


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_filter = ["region"]
    search_fields = ["name", "region__name"]
    list_display = ["name", "region"]


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    class DistrictInline(admin.StackedInline):
        model = District
        extra = 1
    
    inlines = [DistrictInline]
    search_fields = ["name"]
    list_display = ["name", "number_of_districts"]

    admin.display(description="districts")
    def number_of_districts(self, obj):
        return obj.districts.count()