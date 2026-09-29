from datetime import datetime, date

def add_plant(plants: list[dict], name: str, species: str, interval: int) -> None:
    """Добавить новое растение в коллекцию."""
    # Находим максимальный ID, чтобы не было дубликатов
    new_id = max([p['id'] for p in plants], default=0) + 1
    
    new_plant = {
        "id": new_id,
        "name": name,
        "species": species,
        "interval_days": interval,
        "last_watered": str(date.today())
    }
    plants.append(new_plant)
    print(f"Растение '{name}' успешно добавлено (ID: {new_id}).")

def find_plant(plants: list[dict], query: str) -> list[dict]:
    """Найти растения по подстроке в названии."""
    query_lower = query.lower()
    # Используем генератор/списковое включение (расширенные возможности)
    return [p for p in plants if query_lower in p['name'].lower()]

def get_plants_needing_water(plants: list[dict], current_date: date) -> list[dict]:
    """Вернуть список растений, которые пора поливать."""
    needing_water = []
    for plant in plants:
        last_watered = datetime.strptime(plant['last_watered'], "%Y-%m-%d").date()
        days_passed = (current_date - last_watered).days
        
        if days_passed >= plant['interval_days']:
            needing_water.append(plant)
            
    return needing_water

def display_plants(plants: list[dict]) -> None:
    """Вывести все растения в консоль."""
    if not plants:
        print("Коллекция пуста.")
        return
        
    print("\n--- Ваша коллекция растений ---")
    for p in plants:
        print(f"[{p['id']}] {p['name']} ({p['species']}) | "
              f"Полив: раз в {p['interval_days']} дн. | "
              f"Последний полив: {p['last_watered']}")
    print("-------------------------------\n")