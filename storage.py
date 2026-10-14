"""Загрузка и сохранение данных проекта в JSON-файлы."""
import json
import os
from datetime import datetime
from typing import Any, List, Optional, Tuple

from models import Location, Owner, Plant, WateringLog
from models.locations import find_location_by_id
from models.owners import find_owner_by_id
from models.plants import DATE_FORMAT, find_plant_by_id

OWNERS_FILE = "owners.json"
LOCATIONS_FILE = "locations.json"
PLANTS_FILE = "plants.json"
WATERINGS_FILE = "waterings.json"

Dataset = Tuple[
    List[Owner], List[Location], List[Plant], List[WateringLog]
]


def _read_json(filename: str) -> List[dict]:
    """Прочитать список словарей из JSON (при ошибке вернуть [])."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Создан новый список.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON в файле {filename}.")
        return []
    if not isinstance(data, list):
        print(f"Файл {filename}: ожидался список записей.")
        return []
    return data


def _write_json(filename: str, data: List[Any]) -> None:
    """Записать данные в JSON-файл, создав каталог при необходимости."""
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_owners(filename: str) -> List[Owner]:
    """JSON -> объекты Owner."""
    owners = []
    for item in _read_json(filename):
        try:
            owners.append(Owner.from_data(item))
        except (KeyError, TypeError):
            print(f"Пропущена некорректная запись владельца: {item}")
    return owners


def save_owners(filename: str, owners: List[Owner]) -> None:
    """Объекты Owner -> JSON."""
    _write_json(filename, [
        {"id": o.id, "name": o.name, "email": o.email} for o in owners
    ])


def load_locations(filename: str) -> List[Location]:
    """JSON -> объекты Location."""
    locations = []
    for item in _read_json(filename):
        try:
            locations.append(Location.from_data(item))
        except (KeyError, TypeError):
            print(f"Пропущена некорректная запись места: {item}")
    return locations


def save_locations(filename: str, locations: List[Location]) -> None:
    """Объекты Location -> JSON."""
    _write_json(filename, [
        {"id": loc.id, "name": loc.name, "light": loc.light}
        for loc in locations
    ])


def load_plants(
    filename: str,
    owners: Optional[List[Owner]] = None,
    locations: Optional[List[Location]] = None,
) -> List[Plant]:
    """JSON -> объекты Plant со ссылками на Owner и Location."""
    owners = owners or []
    locations = locations or []
    plants = []
    for item in _read_json(filename):
        try:
            datetime.strptime(item["last_watered"], DATE_FORMAT)
            plants.append(Plant(
                plant_id=item["id"],
                name=item["name"],
                species=item["species"],
                interval_days=item["interval_days"],
                last_watered=item["last_watered"],
                owner=find_owner_by_id(owners, item.get("owner_id")),
                location=find_location_by_id(
                    locations, item.get("location_id")
                ),
            ))
        except (KeyError, TypeError, ValueError):
            print(f"Пропущена некорректная запись растения: {item}")
    return plants


def save_plants(filename: str, plants: List[Plant]) -> None:
    """Объекты Plant -> JSON (связи сохраняются как идентификаторы)."""
    _write_json(filename, [
        {
            "id": p.id,
            "name": p.name,
            "species": p.species,
            "interval_days": p.interval_days,
            "last_watered": p.last_watered,
            "owner_id": p.owner.id if p.owner else None,
            "location_id": p.location.id if p.location else None,
        }
        for p in plants
    ])


def load_waterings(
    filename: str,
    plants: List[Plant],
) -> List[WateringLog]:
    """JSON -> объекты WateringLog со ссылкой на Plant."""
    logs = []
    for item in _read_json(filename):
        try:
            plant = find_plant_by_id(plants, item["plant_id"])
            if plant is None:
                print(f"Запись журнала без растения пропущена: {item}")
                continue
            logs.append(WateringLog(
                log_id=item["id"],
                plant=plant,
                watered_on=item["watered_on"],
                note=item.get("note", ""),
            ))
        except (KeyError, TypeError):
            print(f"Пропущена некорректная запись журнала: {item}")
    return logs


def save_waterings(filename: str, logs: List[WateringLog]) -> None:
    """Объекты WateringLog -> JSON."""
    _write_json(filename, [
        {
            "id": log.id,
            "plant_id": log.plant.id,
            "watered_on": log.watered_on,
            "note": log.note,
        }
        for log in logs
    ])


def load_all(data_dir: str) -> Dataset:
    """Загрузить все данные и восстановить связи между объектами."""
    owners = load_owners(os.path.join(data_dir, OWNERS_FILE))
    locations = load_locations(os.path.join(data_dir, LOCATIONS_FILE))
    plants = load_plants(
        os.path.join(data_dir, PLANTS_FILE), owners, locations
    )
    logs = load_waterings(os.path.join(data_dir, WATERINGS_FILE), plants)
    return owners, locations, plants, logs


def save_all(
    data_dir: str,
    owners: List[Owner],
    locations: List[Location],
    plants: List[Plant],
    logs: List[WateringLog],
) -> None:
    """Сохранить все данные проекта."""
    save_owners(os.path.join(data_dir, OWNERS_FILE), owners)
    save_locations(os.path.join(data_dir, LOCATIONS_FILE), locations)
    save_plants(os.path.join(data_dir, PLANTS_FILE), plants)
    save_waterings(os.path.join(data_dir, WATERINGS_FILE), logs)
