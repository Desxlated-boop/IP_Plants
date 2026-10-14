"""Тесты JSON-хранилища: загрузка, сохранение, восстановление связей."""
import json
import os

from storage import load_all, load_plants, save_all


def test_roundtrip_keeps_links(tmp_path):
    root = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(root, "data")
    owners, locations, plants, logs = load_all(data_dir)
    assert owners and locations and plants and logs
    assert plants[0].owner is not None
    assert logs[0].plant in plants

    out = str(tmp_path)
    save_all(out, owners, locations, plants, logs)
    owners2, locations2, plants2, logs2 = load_all(out)
    assert [p.name for p in plants2] == [p.name for p in plants]
    assert plants2[0].owner.id == plants[0].owner.id
    assert plants2[0].location.id == plants[0].location.id
    assert len(logs2) == len(logs)


def test_missing_file_returns_empty_list(tmp_path):
    assert load_plants(str(tmp_path / "nope.json")) == []


def test_broken_json_returns_empty_list(tmp_path):
    broken = tmp_path / "plants.json"
    broken.write_text("{not json", encoding="utf-8")
    assert load_plants(str(broken)) == []


def test_invalid_records_are_skipped(tmp_path):
    path = tmp_path / "plants.json"
    path.write_text(json.dumps([
        {"id": 1, "name": "Ок", "species": "x", "interval_days": 3,
         "last_watered": "2026-10-01"},
        {"id": 2, "name": "Плохая дата", "species": "x",
         "interval_days": 3, "last_watered": "вчера"},
        {"id": 3},
    ]), encoding="utf-8")
    plants = load_plants(str(path))
    assert [p.id for p in plants] == [1]
