"""Класс Plant (растение) и функции работы с коллекцией растений."""
from datetime import date, datetime, timedelta
from typing import List, Optional

from utils import next_id

from .locations import Location
from .owners import Owner

DATE_FORMAT = "%Y-%m-%d"


class Plant:
    """Растение: данные, график полива и связи с владельцем и местом."""

    def __init__(
        self,
        plant_id: int,
        name: str,
        species: str,
        interval_days: int,
        last_watered: str,
        owner: Optional[Owner] = None,
        location: Optional[Location] = None,
    ) -> None:
        """Создать объект растения."""
        self.id = plant_id
        self.name = name
        self.species = species
        self.interval_days = interval_days
        self.last_watered = last_watered
        self.owner = owner
        self.location = location

    def last_watered_date(self) -> date:
        """Вернуть дату последнего полива как объект date."""
        return datetime.strptime(self.last_watered, DATE_FORMAT).date()

    def days_since_watering(self, current_date: date) -> int:
        """Сколько дней прошло с последнего полива."""
        return (current_date - self.last_watered_date()).days

    def needs_watering(self, current_date: date) -> bool:
        """Нужно ли поливать растение в указанную дату."""
        return self.days_since_watering(current_date) >= self.interval_days

    def next_watering_date(self) -> date:
        """Дата следующего плана полива."""
        return self.last_watered_date() + timedelta(days=self.interval_days)

    def water(self, on_date: date) -> None:
        """Отметить полив: обновить дату последнего полива."""
        self.last_watered = on_date.strftime(DATE_FORMAT)

    def __str__(self) -> str:
        """Строковое представление растения."""
        text = (
            f"[{self.id}] {self.name} ({self.species}), "
            f"полив каждые {self.interval_days} дн., "
            f"последний: {self.last_watered}"
        )
        if self.owner is not None:
            text += f", владелец: {self.owner.name}"
        if self.location is not None:
            text += f", место: {self.location.name}"
        return text


def add_plant(
    plants: List[Plant],
    name: str,
    species: str,
    interval_days: int,
    last_watered: Optional[str] = None,
    owner: Optional[Owner] = None,
    location: Optional[Location] = None,
) -> Plant:
    """Создать растение и добавить его в коллекцию."""
    if not name.strip():
        raise ValueError("Название растения не может быть пустым.")
    if interval_days <= 0:
        raise ValueError("Интервал полива должен быть больше нуля.")
    if last_watered is None:
        last_watered = date.today().strftime(DATE_FORMAT)
    plant = Plant(
        next_id(plants),
        name.strip(),
        species.strip(),
        interval_days,
        last_watered,
        owner,
        location,
    )
    plants.append(plant)
    return plant


def find_plant(plants: List[Plant], query: str) -> List[Plant]:
    """Найти растения по части названия."""
    query = query.lower()
    return [plant for plant in plants if query in plant.name.lower()]


def find_plant_by_id(
    plants: List[Plant],
    plant_id: int,
) -> Optional[Plant]:
    """Найти растение по идентификатору."""
    for plant in plants:
        if plant.id == plant_id:
            return plant
    return None


def get_plants_needing_water(
    plants: List[Plant],
    current_date: date,
) -> List[Plant]:
    """Отобрать растения, которые пора поливать."""
    return [
        plant for plant in plants if plant.needs_watering(current_date)
    ]


def filter_plants_by_owner(
    plants: List[Plant],
    owner_id: int,
) -> List[Plant]:
    """Отобрать растения указанного владельца."""
    return [
        plant for plant in plants
        if plant.owner is not None and plant.owner.id == owner_id
    ]


def filter_plants_by_location(
    plants: List[Plant],
    location_id: int,
) -> List[Plant]:
    """Отобрать растения, стоящие в указанном месте."""
    return [
        plant for plant in plants
        if plant.location is not None and plant.location.id == location_id
    ]


def display_plants(plants: List[Plant]) -> None:
    """Вывести растения в консоль."""
    if not plants:
        print("Список растений пуст.")
    for plant in plants:
        print(plant)
