import json
import os

def load_plants(filename: str) -> list[dict]:
    """Загрузить список растений из JSON-файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Создан новый список.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON в файле {filename}. Создан новый список.")
        return []

def save_plants(filename: str, plants: list[dict]) -> None:
    """Сохранить список растений в JSON-файл."""
    # Создаем папку data, если её нет
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(plants, file, ensure_ascii=False, indent=4)