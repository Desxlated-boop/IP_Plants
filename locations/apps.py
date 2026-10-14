"""Конфигурация приложения locations."""
from django.apps import AppConfig


class LocationsConfig(AppConfig):
    """Настройки приложения locations."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "locations"
