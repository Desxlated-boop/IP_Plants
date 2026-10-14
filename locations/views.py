"""Представления приложения locations."""
from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from homepage.data import load_data
from models.locations import find_location_by_id
from models.plants import (
    filter_plants_by_location,
    get_plants_needing_water,
)


def location_list(request: HttpRequest) -> HttpResponse:
    """Страница /locations/: список мест."""
    _, locations, _, _ = load_data()
    return render(
        request,
        "locations/location_list.html",
        {"locations": locations},
    )


def location_detail(
    request: HttpRequest,
    location_id: int,
) -> HttpResponse:
    """Страница /locations/<id>/: место и растения в нём."""
    _, locations, plants, _ = load_data()
    location = find_location_by_id(locations, location_id)
    local_plants = []
    thirsty_ids = set()
    if location is not None:
        local_plants = filter_plants_by_location(plants, location.id)
        thirsty = get_plants_needing_water(local_plants, date.today())
        thirsty_ids = {plant.id for plant in thirsty}
    context = {
        "location": location,
        "plants": local_plants,
        "thirsty_ids": thirsty_ids,
    }
    return render(
        request,
        "locations/location_detail.html",
        context,
        status=404 if location is None else 200,
    )
