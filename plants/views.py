"""Представления приложения plants."""
from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from homepage.data import load_data
from models.plants import find_plant_by_id, get_plants_needing_water
from models.waterings import find_waterings_for_plant


def plant_list(request: HttpRequest) -> HttpResponse:
    """Страница /plants/: список растений."""
    _, _, plants, _ = load_data()
    thirsty = get_plants_needing_water(plants, date.today())
    context = {
        "plants": plants,
        "thirsty_ids": {plant.id for plant in thirsty},
    }
    return render(request, "plants/plant_list.html", context)


def plants_thirsty(request: HttpRequest) -> HttpResponse:
    """Страница /plants/thirsty/: кого пора поливать сегодня."""
    today = date.today()
    _, _, plants, _ = load_data()
    thirsty = get_plants_needing_water(plants, today)
    context = {
        "plants": thirsty,
        "thirsty_ids": {plant.id for plant in thirsty},
        "today": today,
    }
    return render(request, "plants/plants_thirsty.html", context)


def plant_detail(request: HttpRequest, plant_id: int) -> HttpResponse:
    """Страница /plants/<id>/: растение, связи и история поливов."""
    _, _, plants, logs = load_data()
    plant = find_plant_by_id(plants, plant_id)
    thirsty_ids = set()
    history = []
    if plant is not None:
        history = find_waterings_for_plant(logs, plant.id)
        if plant.needs_watering(date.today()):
            thirsty_ids.add(plant.id)
    context = {
        "plant": plant,
        "thirsty_ids": thirsty_ids,
        "waterings": history,
    }
    return render(
        request,
        "plants/plant_detail.html",
        context,
        status=404 if plant is None else 200,
    )
