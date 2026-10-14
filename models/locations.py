"""Класс Location (место в доме) и функции работы с местами."""
from typing import List, Optional

from utils import next_id

LIGHT_LEVELS = ("яркий", "рассеянный", "тень")


class Location:
    """Место, где стоит растение (подоконник, кухня и т. д.)."""

    def __init__(
        self,
        location_id: int,
        name: str,
        light: str = "рассеянный",
    ) -> None:
        """Создать объект места."""
        self.id = location_id
        self.name = name
        self.light = light

    @staticmethod
    def validate_light(light: str) -> bool:
        """Проверить, что уровень освещённости допустим."""
        return light in LIGHT_LEVELS

    @classmethod
    def from_data(cls, data: dict) -> "Location":
        """Создать место из словаря (данные JSON)."""
        return cls(data["id"], data["name"], data["light"])

    def __str__(self) -> str:
        """Строковое представление места."""
        return f"[{self.id}] {self.name} (свет: {self.light})"


def add_location(
    locations: List[Location],
    name: str,
    light: str = "рассеянный",
) -> Location:
    """Создать место и добавить его в коллекцию."""
    if not name.strip():
        raise ValueError("Название места не может быть пустым.")
    if not Location.validate_light(light):
        raise ValueError(
            "Освещённость должна быть: " + ", ".join(LIGHT_LEVELS)
        )
    location = Location(next_id(locations), name.strip(), light)
    locations.append(location)
    return location


def find_location_by_id(
    locations: List[Location],
    location_id: Optional[int],
) -> Optional[Location]:
    """Найти место по идентификатору."""
    for location in locations:
        if location.id == location_id:
            return location
    return None


def display_locations(locations: List[Location]) -> None:
    """Вывести места в консоль."""
    if not locations:
        print("Мест пока нет.")
    for location in locations:
        print(location)
