from django.contrib import admin

from .models import WateringLog


@admin.register(WateringLog)
class WateringLogAdmin(admin.ModelAdmin):
    list_display = ("id", "plant", "watered_on", "note")
    list_select_related = ("plant",)
    search_fields = ("plant__name", "note")
    list_filter = ("watered_on", "plant")
    ordering = ("-watered_on", "-pk")
    list_per_page = 20
