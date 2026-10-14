"""Маршруты приложения plants."""
from django.urls import path

from . import views

app_name = "plants"

urlpatterns = [
    path("", views.plant_list, name="list"),
    # Более специфичный маршрут размещается выше общего <int:...>.
    path("thirsty/", views.plants_thirsty, name="thirsty"),
    path("<int:plant_id>/", views.plant_detail, name="detail"),
]
