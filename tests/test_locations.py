"""Тесты класса Location и функций работы с местами."""
import pytest

from models import Location
from models.locations import add_location, find_location_by_id


def test_location_creation():
    location = Location(1, "Кухня", "рассеянный")
    assert location.name == "Кухня"
    assert "Кухня" in str(location)


def test_validate_light_static_method():
    assert Location.validate_light("яркий")
    assert not Location.validate_light("неон")


def test_add_location_and_find():
    locations = []
    location = add_location(locations, "Спальня", "тень")
    assert find_location_by_id(locations, location.id) is location
    assert find_location_by_id(locations, 99) is None


def test_add_location_invalid_light():
    with pytest.raises(ValueError):
        add_location([], "Балкон", "неон")
