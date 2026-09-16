from datetime import date

# --- Данные растения ---
plant_name = "Фикус"
species = "Ficus"
watering_interval_days = 7
days_since_last_watering = 5
light_requirement = "bright_indirect"

# --- Функции ---

def check_if_needs_watering(days_since, interval):
    """Функция 1: Проверка, нужен ли полив"""
    if days_since >= interval:
        return True
    else:
        return False


def get_location_recommendation(light_req):
    """Функция 2: Рекомендация места"""
    if light_req == "bright_indirect":
        return "Восточное или западное окно"
    elif light_req == "low_light":
        return "Глубина комнаты или северное окно"
    else:
        return "Южное окно с обязательным притенением"


def format_plant_info(name, species, days_since, interval, light_req):
    """Функция 3: Формирование сводки"""
    needs_water = check_if_needs_watering(days_since, interval)
    location = get_location_recommendation(light_req)

    if needs_water:
        status_text = "ТРЕБУЕТ ПОЛИВА!"
        days_left = "0"
    else:
        status_text = "Полив не требуется."
        days_left = str(interval - days_since)

    info = f"--- Карточка растения ---\n"
    info += f"Название: {name} ({species})\n"
    info += f"Статус: {status_text}\n"
    info += f"До следующего полива: {days_left} дн.\n"
    info += f"Рекомендуемое место: {location}\n"
    info += f"Дата проверки: {date.today()}"

    return info


# --- Основной сценарий ---
if __name__ == "__main__":
    plant_card = format_plant_info(
        plant_name,
        species,
        days_since_last_watering,
        watering_interval_days,
        light_requirement
    )
    print(plant_card)