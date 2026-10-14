"""Тесты класса Plant и функций работы с растениями."""
from datetime import date

import pytest

from models import Location, Owner, Plant
from models.plants import (
    add_plant,
    filter_plants_by_location,
    filter_plants_by_owner,
    find_plant,
    find_plant_by_id,
    get_plants_needing_water,
)


def make_plant(last_watered="2026-10-01", interval=7):
    return Plant(1, "Фикус", "Ficus", interval, last_watered)


def test_plant_creation():
    plant = make_plant()
    assert plant.id == 1
    assert plant.name == "Фикус"
    assert plant.owner is None
    assert plant.location is None


def test_plant_str_contains_name_and_links():
    owner = Owner(1, "Анна", "anna@example.com")
    location = Location(1, "Кухня", "яркий")
    plant = Plant(1, "Фикус", "Ficus", 7, "2026-10-01", owner, location)
    text = str(plant)
    assert "Фикус" in text
    assert "Анна" in text
    assert "Кухня" in text


def test_needs_watering_boundary():
    plant = make_plant("2026-10-01", 7)
    assert not plant.needs_watering(date(2026, 10, 7))
    assert plant.needs_watering(date(2026, 10, 8))


def test_next_watering_date_and_water():
    plant = make_plant("2026-10-01", 7)
    assert plant.next_watering_date() == date(2026, 10, 8)
    plant.water(date(2026, 10, 9))
    assert plant.last_watered == "2026-10-09"


def test_add_plant_assigns_ids_and_links():
    plants = []
    owner = Owner(1, "Анна", "anna@example.com")
    first = add_plant(plants, "Фикус", "Ficus", 7, owner=owner)
    second = add_plant(plants, "Кактус", "Echinopsis", 21)
    assert (first.id, second.id) == (1, 2)
    assert first.owner is owner


def test_add_plant_validation():
    with pytest.raises(ValueError):
        add_plant([], "", "Ficus", 7)
    with pytest.raises(ValueError):
        add_plant([], "Фикус", "Ficus", 0)


def test_find_and_filters():
    owner = Owner(1, "Анна", "anna@example.com")
    location = Location(1, "Кухня", "яркий")
    plants = [
        Plant(1, "Фикус", "Ficus", 7, "2026-10-01", owner, location),
        Plant(2, "Кактус", "Echinopsis", 21, "2026-09-28"),
    ]
    assert find_plant(plants, "фик") == [plants[0]]
    assert find_plant_by_id(plants, 2) is plants[1]
    assert find_plant_by_id(plants, 99) is None
    assert filter_plants_by_owner(plants, 1) == [plants[0]]
    assert filter_plants_by_location(plants, 1) == [plants[0]]


def test_get_plants_needing_water():
    plants = [
        make_plant("2026-10-01", 7),
        Plant(2, "Кактус", "Echinopsis", 21, "2026-10-10"),
    ]
    result = get_plants_needing_water(plants, date(2026, 10, 13))
    assert result == [plants[0]]
