# IP_Plants — Сервис учета домашних коллекций растений

## Назначение

Приложение для учета домашних растений, графика полива и журнала поливов. Есть консольная версия и веб-интерфейс на Django.

## Целевая аудитория

Любители комнатных растений, начинающие садоводы, люди, которые хотят систематизировать уход за своими цветами.

## Предметная область

Домашнее цветоводство: коллекция растений, их владельцы, места в доме (с разным освещением) и история поливов.

## Основные функции

- просмотр коллекции растений, добавление растения, поиск по названию;
- определение растений, которые пора поливать сегодня;
- отметка полива с записью в журнал (дата последнего полива обновляется);
- учет владельцев и мест, просмотр растений владельца и места;
- хранение данных между запусками в JSON;
- веб-интерфейс: списки и карточки растений, владельцев, мест, журнал поливов.

## Объектная модель (ООП)

Четыре класса пакета `models/`:

```text
Owner  <──  Plant  ──>  Location
              ^
              │
         WateringLog
```

| Класс | Атрибуты | Методы |
|-------|----------|--------|
| `Owner` | `id`, `name`, `email` | `from_data()` (classmethod), `__str__()` |
| `Location` | `id`, `name`, `light` | `validate_light()` (staticmethod), `from_data()`, `__str__()` |
| `Plant` | `id`, `name`, `species`, `interval_days`, `last_watered`, `owner`, `location` | `needs_watering()`, `days_since_watering()`, `next_watering_date()`, `water()`, `__str__()` |
| `WateringLog` | `id`, `plant`, `watered_on`, `note` | `__str__()` |

**Взаимодействие объектов:** `Plant` хранит ссылки на `Owner` и `Location` (композиция), `WateringLog` хранит ссылку на `Plant`. Функция `add_watering()` создает запись журнала и обновляет `Plant.last_watered`.

Функции работы с коллекциями (`add_plant`, `find_plant`, `find_plant_by_id`, `get_plants_needing_water`, `filter_plants_by_owner`, `filter_plants_by_location`, `add_owner`, `add_location`, `find_waterings_for_plant`, ...) лежат рядом с классами и принимают `List[...]` объектов.

## Хранение данных

Каталог `data/`: `owners.json`, `locations.json`, `plants.json`, `waterings.json`. Связи хранятся как идентификаторы (`owner_id`, `location_id`, `plant_id`). При загрузке (`storage.load_all`) JSON преобразуется в объекты, ссылки восстанавливаются; при сохранении объекты преобразуются обратно в данные. Некорректные записи пропускаются с сообщением, отсутствующий или поврежденный файл не приводит к аварийному завершению.

## Веб-интерфейс (Django 5.2)

| URL | Имя маршрута | Что показывает |
|-----|--------------|----------------|
| `/` | `homepage:index` | главная, сводка по коллекции |
| `/plants/` | `plants:list` | список растений |
| `/plants/thirsty/` | `plants:thirsty` | кого пора поливать |
| `/plants/<id>/` | `plants:detail` | карточка растения, владелец, место, история поливов |
| `/owners/` | `owners:list` | владельцы |
| `/owners/<id>/` | `owners:detail` | владелец и его растения |
| `/locations/` | `locations:list` | места |
| `/locations/<id>/` | `locations:detail` | место и растения в нем |
| `/waterings/` | `waterings:list` | журнал поливов |

Для несуществующих объектов страницы возвращают код 404; для неизвестных адресов настроен `handler404`.

**Шаблоны Django:** базовый `templates/base.html` (блоки `title`, `content`), наследование `{% extends %}`, включаемые шаблоны (`includes/navigation.html`, `plants/includes/plant_card.html`, `plants/includes/watering_status.html`), контекст из view-функций, `{% for %}…{% empty %}`, `{% if %}`, фильтры (`length`, `default`, `date`), именованные URL с пространствами имён, статические файлы (`homepage/static/homepage/`: `css/style.css`, `js/main.js`, `img/logo.png`), Bootstrap 5.3 через CDN.

Django ORM, формы и база данных пока не используются — данные берутся из JSON.

## Структура проекта

```text
IP_Plants/
├── manage.py
├── plantly/                 # конфигурация Django-проекта
├── homepage/                # главная, загрузка данных, статика, 404
├── plants/  owners/  locations/  waterings/   # Django-приложения
├── templates/               # base.html, 404.html, includes/
├── models/                  # классы предметной области
│   ├── owners.py  locations.py  plants.py  waterings.py
├── data/                    # JSON-хранилище
├── tests/                   # pytest
├── main.py                  # консольная версия
├── storage.py               # JSON <-> объекты
├── utils.py                 # ввод, next_id
├── requirements.txt
└── README.md
```

## Запуск

```text
pip install -r requirements.txt
python main.py                 # консольная версия
python manage.py migrate
python manage.py runserver     # веб-версия: http://127.0.0.1:8000/
```

## Тестирование и качество кода

```text
pytest -v
flake8 . --extend-exclude=venv
python manage.py check
```

## План развития

Реализовано: ООП-модель из четырех классов, JSON-хранилище, консольное меню, Django-проект с шаблонным интерфейсом.

Планируется:

- модели Django и база данных (ORM);
- формы создания и редактирования растений, владельцев, мест, поливов;
- регистрация и авторизация пользователей;
- REST API;
- контейнеризация (Docker);
- CI/CD.
