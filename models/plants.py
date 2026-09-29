from datetime import date, datetime
from typing import List


class Plant:
    """Класс, описывающий домашнее растение."""

    def __init__(
        self,
        plant_id: int,
        name: str,
        species: str,
        interval_days: int,
        last_watered: str
    ) -> None:
        self.id = plant_id
        self.name = name
        self.species = species
        self.interval_days = interval_days
        self.last_watered = last_watered

    def needs_watering(self, current_date: date) -> bool:
        """Метод объекта: проверяет, нужен ли полив именно этому растению."""
        last = datetime.strptime(self.last_watered, "%Y-%m-%d").date()
        days_passed = (current_date - last).days
        return days_passed >= self.interval_days

    def __str__(self) -> str:
        """Строковое представление объекта."""
        return (
            f"[{self.id}] {self.name} ({self.species}) | "
            f"Полив: раз в {self.interval_days} дн. | "
            f"Последний полив: {self.last_watered}"
        )


# --- Функции работы с коллекцией объектов (остаются обычными функциями) ---

def add_plant(
        plants: List[Plant],
        name: str,
        species: str,
        interval: int) -> None:
    """Добавить новое растение в коллекцию."""
    new_id = max([p.id for p in plants], default=0) + 1
    new_plant = Plant(new_id, name, species, interval, str(date.today()))
    plants.append(new_plant)
    print(f"Растение '{name}' успешно добавлено (ID: {new_id}).")


def find_plant(plants: List[Plant], query: str) -> List[Plant]:
    """Найти растения по подстроке в названии."""
    query_lower = query.lower()
    return [p for p in plants if query_lower in p.name.lower()]


def get_plants_needing_water(
        plants: List[Plant],
        current_date: date) -> List[Plant]:
    """Вернуть список растений, которые пора поливать."""
    return [p for p in plants if p.needs_watering(current_date)]


def display_plants(plants: List[Plant]) -> None:
    """Вывести все растения в консоль."""
    if not plants:
        print("Коллекция пуста.")
        return

    print("\n--- Ваша коллекция растений ---")
    for p in plants:
        print(p)  # Здесь автоматически вызовется метод __str__
    print("-------------------------------\n")
