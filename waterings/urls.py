"""Маршруты приложения waterings."""
from django.urls import path

from . import views

app_name = "waterings"

urlpatterns = [
    path("", views.watering_list, name="list"),
]
