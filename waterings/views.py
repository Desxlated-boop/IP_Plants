"""Представления приложения waterings."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from homepage.data import load_data
from models.waterings import sort_waterings


def watering_list(request: HttpRequest) -> HttpResponse:
    """Страница /waterings/: журнал поливов (новые первыми)."""
    _, _, _, logs = load_data()
    return render(
        request,
        "waterings/watering_list.html",
        {"logs": sort_waterings(logs)},
    )
