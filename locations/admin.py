from django.contrib import admin

from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "light")
    search_fields = ("name",)
    list_filter = ("light",)
    ordering = ("name",)
    list_per_page = 20
