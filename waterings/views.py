"""Представления приложения waterings."""
from datetime import date

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from homepage.data import load_data
from models.plants import get_plants_needing_water
from models.waterings import find_watering_by_id, sort_waterings


def watering_list(request: HttpRequest) -> HttpResponse:
    """Страница /waterings/: журнал поливов (новые первыми)."""
    owners, _, plants, logs = load_data()
    thirsty = get_plants_needing_water(plants, date.today())
    query = request.GET.get("q", "").strip()
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()
    sorting = request.GET.get("sort", "newest")
    owner_id = request.GET.get("owner", "")
    plant_id = request.GET.get("plant", "")
    error = ""
    try:
        if date_from:
            date.fromisoformat(date_from)
        if date_to:
            date.fromisoformat(date_to)
    except ValueError:
        error = "Введите корректную дату."
        date_from = date_to = ""
    if isinstance(logs, QuerySet):
        if query:
            logs = logs.filter(plant__name__icontains=query)
        if owner_id.isdigit():
            logs = logs.filter(plant__owner_id=int(owner_id))
        if plant_id.isdigit():
            logs = logs.filter(plant_id=int(plant_id))
        if date_from:
            logs = logs.filter(watered_on__gte=date_from)
        if date_to:
            logs = logs.filter(watered_on__lte=date_to)
        if sorting == "oldest":
            logs = logs.order_by("watered_on", "pk")
        else:
            logs = logs.order_by("-watered_on", "-pk")
    else:
        logs = sort_waterings(logs)
    page = Paginator(logs, 10).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    context = {
        "logs": page,
        "thirsty_ids": {plant.id for plant in thirsty},
        "query": query,
        "date_from": date_from,
        "date_to": date_to,
        "sorting": sorting,
        "owners": owners,
        "plants": plants,
        "owner_id": owner_id,
        "plant_id": plant_id,
        "error": error,
        "page": page,
        "page_params": params.urlencode(),
    }
    return render(
        request,
        "waterings/watering_list.html",
        context,
    )


def watering_detail(request: HttpRequest, log_id: int) -> HttpResponse:
    """Страница /waterings/<id>/: сведения об отдельном поливе."""
    _, _, plants, logs = load_data()
    log = find_watering_by_id(logs, log_id)
    thirsty = get_plants_needing_water(plants, date.today())
    context = {
        "log": log,
        "thirsty_ids": {plant.id for plant in thirsty},
    }
    return render(
        request,
        "waterings/watering_detail.html",
        context,
        status=404 if log is None else 200,
    )
