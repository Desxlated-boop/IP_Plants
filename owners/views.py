"""Представления приложения owners."""
from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from homepage.data import load_data
from models.owners import find_owner_by_id
from models.plants import filter_plants_by_owner, get_plants_needing_water


def owner_list(request: HttpRequest) -> HttpResponse:
    """Страница /owners/: список владельцев."""
    owners, _, _, _ = load_data()
    return render(request, "owners/owner_list.html", {"owners": owners})


def owner_detail(request: HttpRequest, owner_id: int) -> HttpResponse:
    """Страница /owners/<id>/: владелец и его растения."""
    owners, _, plants, _ = load_data()
    owner = find_owner_by_id(owners, owner_id)
    own_plants = []
    thirsty_ids = set()
    if owner is not None:
        own_plants = filter_plants_by_owner(plants, owner.id)
        thirsty = get_plants_needing_water(own_plants, date.today())
        thirsty_ids = {plant.id for plant in thirsty}
    context = {
        "owner": owner,
        "plants": own_plants,
        "thirsty_ids": thirsty_ids,
    }
    return render(
        request,
        "owners/owner_detail.html",
        context,
        status=404 if owner is None else 200,
    )
