"""Тесты класса WateringLog и журнала поливов."""
from datetime import date

from models import Plant, WateringLog
from models.waterings import (
    add_watering,
    find_waterings_for_plant,
    sort_waterings,
)


def make_plant():
    return Plant(1, "Фикус", "Ficus", 7, "2026-10-01")


def test_watering_log_links_to_plant():
    plant = make_plant()
    log = WateringLog(1, plant, "2026-10-02", "тест")
    assert log.plant is plant
    assert "Фикус" in str(log)


def test_add_watering_updates_plant():
    plant = make_plant()
    logs = []
    log = add_watering(logs, plant, date(2026, 10, 10), "полив")
    assert logs == [log]
    assert plant.last_watered == "2026-10-10"


def test_old_watering_does_not_rewind_plant():
    plant = make_plant()
    add_watering([], plant, date(2026, 9, 1))
    assert plant.last_watered == "2026-10-01"


def test_find_and_sort_waterings():
    plant = make_plant()
    other = Plant(2, "Кактус", "Echinopsis", 21, "2026-10-01")
    logs = []
    add_watering(logs, plant, date(2026, 10, 2))
    add_watering(logs, other, date(2026, 10, 3))
    add_watering(logs, plant, date(2026, 10, 5))
    own = find_waterings_for_plant(logs, plant.id)
    assert [log.watered_on for log in own] == ["2026-10-05", "2026-10-02"]
    assert sort_waterings(logs)[0].watered_on == "2026-10-05"
