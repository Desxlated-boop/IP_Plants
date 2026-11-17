from django.contrib import admin
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from waterings.models import WateringLog
from .models import Plant


@admin.action(description="Отметить полив сегодня")
def water_today(modeladmin, request, queryset):
    today = timezone.localdate()
    plants = list(queryset.filter(last_watered__lte=today))
    with transaction.atomic():
        WateringLog.objects.bulk_create([
            WateringLog(plant=plant, watered_on=today, note="Через админку")
            for plant in plants
        ])
        queryset.filter(pk__in=[plant.pk for plant in plants]).update(
            last_watered=today
        )
    modeladmin.message_user(request, f"Полито растений: {len(plants)}.")


@admin.action(description="Увеличить интервал полива на один день")
def extend_interval(modeladmin, request, queryset):
    count = queryset.update(interval_days=F("interval_days") + 1)
    modeladmin.message_user(request, f"Изменено растений: {count}.")


class WateringInline(admin.TabularInline):
    model = WateringLog
    extra = 0


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "species", "owner", "location", "interval_days",
        "is_infrequent",
    )
    list_display_links = ("id", "name")
    list_editable = ("interval_days",)
    list_select_related = ("owner", "location")
    search_fields = ("name", "species", "owner__name")
    list_filter = ("owner", "location", "is_infrequent")
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("is_infrequent",)
    inlines = (WateringInline,)
    actions = (water_today, extend_interval)
