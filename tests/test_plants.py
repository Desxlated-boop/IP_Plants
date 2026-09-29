from datetime import date, timedelta
from plants import add_plant, find_plant, get_plants_needing_water

def test_add_plant():
    """Тест добавления растения."""
    plants = []
    add_plant(plants, "Фикус", "Ficus", 7)
    assert len(plants) == 1
    assert plants[0]["name"] == "Фикус"
    assert plants[0]["id"] == 1

def test_find_plant():
    """Тест поиска по подстроке."""
    plants = []
    add_plant(plants, "Фикус Бенджамина", "Ficus", 7)
    add_plant(plants, "Кактус", "Mammillaria", 14)
    
    results = find_plant(plants, "фикус")
    assert len(results) == 1
    assert results[0]["name"] == "Фикус Бенджамина"

def test_get_plants_needing_water():
    """Тест проверки необходимости полива."""
    today = date.today()
    # Создаем растение, которое поливали 10 дней назад (интервал 7 дней)
    plants = [{
        "id": 1, 
        "name": "Тестовое", 
        "species": "Test", 
        "interval_days": 7, 
        "last_watered": str(today - timedelta(days=10))
    }]
    
    needing = get_plants_needing_water(plants, today)
    assert len(needing) == 1
    
    # А теперь проверим растение, которое поливали вчера
    plants[0]["last_watered"] = str(today - timedelta(days=1))
    needing = get_plants_needing_water(plants, today)
    assert len(needing) == 0