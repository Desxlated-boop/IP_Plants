"""Проверка веб-страниц Django: коды ответов основных URL."""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plantly.settings")
django.setup()

from django.test import Client  # noqa: E402


def make_client() -> Client:
    """Создать тестовый клиент с разрешённым именем хоста."""
    return Client(HTTP_HOST="localhost")


def test_existing_pages_return_200():
    client = make_client()
    for url in (
        "/",
        "/plants/",
        "/plants/thirsty/",
        "/plants/1/",
        "/owners/",
        "/owners/1/",
        "/locations/",
        "/locations/1/",
        "/waterings/",
    ):
        assert client.get(url).status_code == 200, url


def test_missing_objects_return_404():
    client = make_client()
    for url in (
        "/plants/999999/",
        "/owners/999999/",
        "/locations/999999/",
        "/nonexistent/",
    ):
        assert client.get(url).status_code == 404, url


def test_plant_page_shows_related_objects():
    html = make_client().get("/plants/1/").content.decode("utf-8")
    assert "Фикус" in html
    assert "Анна" in html
