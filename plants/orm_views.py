"""Статистика по актуальным данным Django ORM."""
from django.db.models import Count
from django.shortcuts import render

from locations.models import Location
from owners.models import Owner
from plants.models import Plant
from waterings.models import WateringLog


def statistics(request):
    """Количество растений и поливов с группировкой по связям."""
    context = {
        "plant_total": Plant.objects.count(),
        "watering_total": WateringLog.objects.count(),
        "frequent_total": Plant.objects.frequent_watering().count(),
        "owners": Owner.objects.annotate(plant_count=Count("plants")),
        "locations": Location.objects.annotate(plant_count=Count("plants")),
        "plants": Plant.objects.with_watering_count(),
    }
    return render(request, "plants/orm_statistics.html", context)
