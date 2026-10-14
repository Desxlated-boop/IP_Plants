"""Консольная версия приложения IP_Plants."""
from datetime import date
from typing import List, Optional

from models import Location, Owner, Plant, WateringLog
from models.locations import (
    add_location,
    display_locations,
    find_location_by_id,
)
from models.owners import (
    add_owner,
    display_owners,
    find_owner_by_id,
)
from models.plants import (
    add_plant,
    display_plants,
    find_plant,
    find_plant_by_id,
    get_plants_needing_water,
)
from models.waterings import add_watering, display_waterings
from storage import load_all, save_all
from utils import input_int

DATA_DIR = "data"

MENU = """
=== IP_Plants: Учет домашних растений ===
1. Показать все растения
2. Добавить растение
3. Найти растение
4. Проверить, кого пора поливать
5. Полить растение (запись в журнал)
6. Показать журнал поливов
7. Владельцы (показать / добавить)
8. Места (показать / добавить)
0. Выход"""


def choose_owner(owners: List[Owner]) -> Optional[Owner]:
    """Выбрать владельца по id (0 - без владельца)."""
    display_owners(owners)
    owner_id = input_int("ID владельца (0 - без владельца): ")
    return find_owner_by_id(owners, owner_id)


def choose_location(locations: List[Location]) -> Optional[Location]:
    """Выбрать место по id (0 - без места)."""
    display_locations(locations)
    location_id = input_int("ID места (0 - без места): ")
    return find_location_by_id(locations, location_id)


def handle_add_plant(
    plants: List[Plant],
    owners: List[Owner],
    locations: List[Location],
) -> None:
    """Сценарий добавления растения."""
    name = input("Название растения (например, Фикус): ")
    species = input("Вид (например, Ficus): ")
    interval = input_int("Интервал полива (в днях): ")
    owner = choose_owner(owners)
    location = choose_location(locations)
    try:
        plant = add_plant(
            plants, name, species, interval,
            owner=owner, location=location,
        )
    except ValueError as error:
        print(f"Ошибка: {error}")
        return
    print(f"Добавлено: {plant}")


def handle_water(
    plants: List[Plant],
    logs: List[WateringLog],
) -> None:
    """Сценарий полива: запись в журнал и обновление растения."""
    display_plants(plants)
    plant = find_plant_by_id(plants, input_int("ID растения: "))
    if plant is None:
        print("Растение не найдено.")
        return
    note = input("Заметка (можно пусто): ")
    log = add_watering(logs, plant, date.today(), note)
    print(f"Записано: {log}")


def handle_owners(owners: List[Owner]) -> None:
    """Сценарий работы с владельцами."""
    display_owners(owners)
    if input("Добавить владельца? (y/n): ").lower() != "y":
        return
    name = input("Имя: ")
    email = input("E-mail: ")
    try:
        print(f"Добавлен: {add_owner(owners, name, email)}")
    except ValueError as error:
        print(f"Ошибка: {error}")


def handle_locations(locations: List[Location]) -> None:
    """Сценарий работы с местами."""
    display_locations(locations)
    if input("Добавить место? (y/n): ").lower() != "y":
        return
    name = input("Название места: ")
    light = input("Освещённость (яркий / рассеянный / тень): ")
    try:
        print(f"Добавлено: {add_location(locations, name, light)}")
    except ValueError as error:
        print(f"Ошибка: {error}")


def main() -> None:
    """Главный цикл приложения."""
    owners, locations, plants, logs = load_all(DATA_DIR)

    while True:
        print(MENU)
        choice = input_int("Выберите действие: ")

        if choice == 1:
            display_plants(plants)
        elif choice == 2:
            handle_add_plant(plants, owners, locations)
        elif choice == 3:
            query = input("Введите часть названия для поиска: ")
            display_plants(find_plant(plants, query))
        elif choice == 4:
            today = date.today()
            thirsty = get_plants_needing_water(plants, today)
            if thirsty:
                print(f"\nВнимание! Сегодня ({today}) требуют полива:")
                display_plants(thirsty)
            else:
                print("\nПолив не требуется.")
        elif choice == 5:
            handle_water(plants, logs)
        elif choice == 6:
            display_waterings(logs)
        elif choice == 7:
            handle_owners(owners)
        elif choice == 8:
            handle_locations(locations)
        elif choice == 0:
            print("Сохраняем данные и выходим...")
            break
        else:
            print("Неизвестная команда.")
        save_all(DATA_DIR, owners, locations, plants, logs)

    save_all(DATA_DIR, owners, locations, plants, logs)


if __name__ == "__main__":
    main()
