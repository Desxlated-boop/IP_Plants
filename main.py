from datetime import date

from models.plants import (
    add_plant,
    display_plants,
    find_plant,
    get_plants_needing_water,
)
from storage import load_plants, save_plants
from utils import input_int

DATA_FILE = "data/plants.json"


def main() -> None:
    """Главный цикл приложения."""
    plants = load_plants(DATA_FILE)

    while True:
        print("\n=== IP_Plants: Учет домашних растений (ООП) ===")
        print("1. Показать все растения")
        print("2. Добавить растение")
        print("3. Найти растение")
        print("4. Проверить, кого пора поливать")
        print("0. Выход")

        choice = input_int("Выберите действие: ")

        if choice == 1:
            display_plants(plants)

        elif choice == 2:
            name = input("Название растения (например, Фикус): ")
            species = input("Вид (например, Ficus): ")
            interval = input_int("Интервал полива (в днях): ")
            add_plant(plants, name, species, interval)
            save_plants(DATA_FILE, plants)

        elif choice == 3:
            query = input("Введите часть названия для поиска: ")
            results = find_plant(plants, query)
            display_plants(results)

        elif choice == 4:
            today = date.today()
            thirsty = get_plants_needing_water(plants, today)
            if thirsty:
                print(f"\nВнимание! Сегодня ({today}) требуют полива:")
                display_plants(thirsty)
            else:
                print("\nПолив не требуется.")

        elif choice == 0:
            print("Сохраняем данные и выходим...")
            save_plants(DATA_FILE, plants)
            break

        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
