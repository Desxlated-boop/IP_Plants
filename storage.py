import json
import os
from typing import List
from models.plants import Plant


def load_plants(filename: str) -> List[Plant]:
    """Загрузить список растений из JSON и преобразовать в объекты Plant."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

            plants = []
            for item in data:
                plant = Plant(
                    plant_id=item["id"],
                    name=item["name"],
                    species=item["species"],
                    interval_days=item["interval_days"],
                    last_watered=item["last_watered"]
                )
                plants.append(plant)
            return plants

    except FileNotFoundError:
        print(f"Файл {filename} не найден. Создан новый список.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON в файле {filename}.")
        return []


def save_plants(filename: str, plants: List[Plant]) -> None:
    """Преобразовать объекты Plant в словари и сохранить в JSON."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Преобразуем объекты обратно в словари для JSON
    data = []
    for p in plants:
        data.append({
            "id": p.id,
            "name": p.name,
            "species": p.species,
            "interval_days": p.interval_days,
            "last_watered": p.last_watered
        })

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
