from datetime import date, timedelta
from models.plants import (
    Plant,
    add_plant,
    find_plant,
)


def test_plant_creation():
    """Тест создания объекта Plant."""
    plant = Plant(1, "Фикус", "Ficus", 7, "2026-09-20")
    assert plant.id == 1
    assert plant.name == "Фикус"
    assert plant.interval_days == 7


def test_plant_needs_watering():
    """Тест метода needs_watering."""
    today = date.today()
    # Растение поливали 8 дней назад, интервал 7 -> нужен полив
    plant_thirsty = Plant(1, "Фикус", "Ficus", 7,
                          str(today - timedelta(days=8)))
    assert plant_thirsty.needs_watering(today) is True

    # Растение поливали вчера -> полив не нужен
    plant_happy = Plant(2, "Кактус", "Cactus", 14,
                        str(today - timedelta(days=1)))
    assert plant_happy.needs_watering(today) is False


def test_add_plant_to_collection():
    """Тест добавления объекта в коллекцию."""
    plants = []
    add_plant(plants, "Фикус", "Ficus", 7)
    assert len(plants) == 1
    # Проверяем, что это именно объект, а не словарь
    assert isinstance(plants[0], Plant)


def test_find_plant():
    """Тест поиска по коллекции объектов."""
    plants = []
    add_plant(plants, "Фикус Бенджамина", "Ficus", 7)
    add_plant(plants, "Кактус", "Mammillaria", 14)

    results = find_plant(plants, "фикус")
    assert len(results) == 1
    assert results[0].name == "Фикус Бенджамина"
