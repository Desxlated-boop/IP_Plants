"""Представления главной страницы и страницы 404."""
from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from homepage.data import load_data
from models.plants import get_plants_needing_water


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница со сводкой по коллекции."""
    owners, locations, plants, logs = load_data()
    thirsty = get_plants_needing_water(plants, date.today())
    context = {
        "plants_count": len(plants),
        "owners_count": len(owners),
        "locations_count": len(locations),
        "thirsty_count": len(thirsty),
    }
    return render(request, "homepage/index.html", context)


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    """Собственная страница 404 (работает при DEBUG = False)."""
    return render(request, "404.html", status=404)
