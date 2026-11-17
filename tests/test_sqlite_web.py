"""Проверки импорта и страниц SQLite на изолированных данных."""
import json
import os
import sqlite3

import django
import pytest

from db.database import get_connection
from db.import_json import import_data
from db.queries import get_queries

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plantly.settings")
django.setup()

from django.test import Client  # noqa: E402


def make_client():
    return Client(HTTP_HOST="localhost")


@pytest.fixture
def collection(tmp_path, monkeypatch):
    data = {
        "owners": [{"id": 1, "name": "Анна", "email": ""}],
        "locations": [{"id": 1, "name": "Окно", "light": "яркий"}],
        "plants": [
            {"id": 1, "name": "Фикус", "species": "Ficus",
             "interval_days": 7, "last_watered": "2026-10-01",
             "owner_id": 1, "location_id": 1},
            {"id": 2, "name": "Кактус", "species": "Cactus",
             "interval_days": 21, "last_watered": "2026-10-01",
             "owner_id": None, "location_id": None},
        ],
        "waterings": [
            {"id": 1, "plant_id": 1, "watered_on": "2026-10-01",
             "note": "по графику"},
        ],
    }
    for name, entries in data.items():
        (tmp_path / (name + ".json")).write_text(
            json.dumps(entries, ensure_ascii=False), encoding="utf-8"
        )
    db_path = tmp_path / "collection.sqlite"
    assert import_data(tmp_path, db_path)["plants"] == 2
    monkeypatch.setattr(
        "plants.sql_views.get_connection",
        lambda read_only: get_connection(db_path, read_only=read_only),
    )
    return tmp_path, db_path


def test_queries_and_foreign_keys(collection):
    _, db_path = collection
    conn = get_connection(db_path)
    try:
        queries = get_queries()
        assert len(queries) >= 10
        parameters = {
            "due_on_date": ("2026-10-10",),
            "plants_by_light": ("яркий",),
            "watering_by_plant": (1,),
            "recent_waterings": (3, 0),
        }
        for name, sql in queries.items():
            conn.execute(sql, parameters.get(name, ())).fetchall()
        assert conn.execute(queries["plant_total"]).fetchone()["total"] == 2
        assert conn.execute(queries["plants_list"]).fetchall()[0]["name"]
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO waterings VALUES (2, 999, ?, ?)",
                         ("2026-10-10", ""))
    finally:
        conn.close()


def test_import_refuses_existing_data(collection):
    data_dir, db_path = collection
    with pytest.raises(ValueError, match="импорт отменён"):
        import_data(data_dir, db_path)
    conn = get_connection(db_path)
    try:
        assert conn.execute("SELECT COUNT(*) FROM plants").fetchone()[0] == 2
    finally:
        conn.close()


def test_bad_reference_rolls_back_import(collection):
    data_dir, _ = collection
    (data_dir / "waterings.json").write_text(
        json.dumps([{"id": 1, "plant_id": 999, "watered_on": "2026-10-01"}]),
        encoding="utf-8",
    )
    db_path = data_dir / "invalid.sqlite"
    with pytest.raises(sqlite3.IntegrityError):
        import_data(data_dir, db_path)
    conn = get_connection(db_path)
    try:
        for table in ("owners", "locations", "plants", "waterings"):
            count = conn.execute("SELECT COUNT(*) FROM " + table).fetchone()[0]
            assert count == 0
    finally:
        conn.close()


def test_sqlite_pages_and_date_search(collection):
    client = make_client()
    for url in ("/plants/database/", "/plants/database/plants/",
                "/plants/database/waterings/", "/plants/database/search/",
                "/plants/database/statistics/"):
        assert client.get(url).status_code == 200
    response = client.get("/plants/database/search/", {"date": "2026-10-10"})
    html = response.content.decode("utf-8")
    assert "Фикус" in html
    assert "Кактус" not in html
    html = client.get("/plants/database/search/", {
        "date": "2026-02-30"
    }).content.decode("utf-8")
    assert "Введите корректную дату" in html
    html = client.get("/plants/database/statistics/").content.decode("utf-8")
    assert "Растений: 2" in html
    assert "Анна: 1" in html


def test_missing_database_shows_help(tmp_path, monkeypatch):
    db_path = tmp_path / "missing.sqlite"
    monkeypatch.setattr(
        "plants.sql_views.get_connection",
        lambda read_only: get_connection(db_path, read_only=read_only),
    )
    response = make_client().get("/plants/database/")
    assert response.status_code == 503
    assert "python -m db.import_json" in response.content.decode("utf-8")
    assert not db_path.exists()
