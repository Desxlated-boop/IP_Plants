"""Маршруты приложения waterings."""
from django.urls import path

from . import views

app_name = "waterings"

urlpatterns = [
    path("", views.watering_list, name="list"),
    path("<int:log_id>/", views.watering_detail, name="detail"),
]
