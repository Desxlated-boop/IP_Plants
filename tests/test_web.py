"""Проверка веб-страниц Django: коды ответов основных URL."""
import os
from datetime import date, timedelta

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plantly.settings")
django.setup()

from django.test import Client, override_settings  # noqa: E402
from django.urls import reverse  # noqa: E402

from models import Location, Owner, Plant, WateringLog  # noqa: E402


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
        "/waterings/1/",
    ):
        assert client.get(url).status_code == 200, url


def test_missing_objects_return_404():
    client = make_client()
    for url in (
        "/plants/999999/",
        "/owners/999999/",
        "/locations/999999/",
        "/waterings/999999/",
        "/nonexistent/",
    ):
        assert client.get(url).status_code == 404, url


def test_plant_page_shows_related_objects():
    html = make_client().get("/plants/1/").content.decode("utf-8")
    assert "Фикус" in html
    assert "Анна" in html


@pytest.fixture
def watering_data(monkeypatch):
    """Данные для проверки страниц без изменения JSON-файлов проекта."""
    today = date.today()
    owner = Owner(1, "Анна", "anna@example.com")
    location = Location(1, "Подоконник", "яркий")
    plants = [
        Plant(1, "Фикус", "Ficus", 7, today.isoformat(), owner, location),
        Plant(2, "Кактус", "", 7, (today - timedelta(days=10)).isoformat()),
    ]
    logs = [
        WateringLog(1, plants[0], today.isoformat(), "<b>Утренний полив</b>"),
        WateringLog(2, plants[1], plants[1].last_watered),
    ]
    dataset = ([owner], [location], plants, logs)
    monkeypatch.setattr("waterings.views.load_data", lambda: dataset)
    return dataset


def test_watering_detail_shows_data_and_links(watering_data):
    log = watering_data[3][0]
    url = reverse("waterings:detail", args=[log.id])
    response = make_client().get(url)
    html = response.content.decode("utf-8")
    assert response.status_code == 200
    for text in ("Полив №1", "Фикус", "Анна", "Подоконник", log.watered_on):
        assert text in html
    for route in ("/plants/1/", "/owners/1/", "/locations/1/", "/waterings/"):
        assert f'href="{route}"' in html
    assert "&lt;b&gt;Утренний полив&lt;/b&gt;" in html
    assert "<b>Утренний полив</b>" not in html


def test_watering_list_links_to_details(watering_data):
    html = make_client().get("/waterings/").content.decode("utf-8")
    assert 'href="/waterings/1/"' in html
    assert 'href="/waterings/2/"' in html
    assert "Всего записей: 2" in html
    assert html.index('href="/waterings/1/"') < html.index(
        'href="/waterings/2/"'
    )


@pytest.mark.parametrize("log_id, status", [
    (1, "Полив не нужен"),
    (2, "Пора поливать"),
])
def test_watering_status_in_list_and_detail(watering_data, log_id, status):
    client = make_client()
    for url in ("/waterings/", f"/waterings/{log_id}/"):
        assert status in client.get(url).content.decode("utf-8")


def test_watering_detail_without_optional_values(watering_data):
    html = make_client().get("/waterings/2/").content.decode("utf-8")
    assert "без заметки" in html
    assert "не указан" in html
    assert "не указано" in html


def test_empty_watering_list_and_missing_record(monkeypatch):
    monkeypatch.setattr("waterings.views.load_data", lambda: ([], [], [], []))
    client = make_client()
    html = client.get("/waterings/").content.decode("utf-8")
    assert "Записей пока нет." in html
    response = client.get("/waterings/1/")
    assert response.status_code == 404
    assert "Запись о поливе не найдена" in response.content.decode("utf-8")


@override_settings(DEBUG=False)
def test_custom_404_page():
    client = make_client()
    for url in ("/nonexistent/", "/waterings/text/"):
        response = client.get(url)
        assert response.status_code == 404
        assert "Проверьте адрес" in response.content.decode("utf-8")
