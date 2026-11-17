"""Создание таблиц и однократный перенос данных из JSON в SQLite."""
import json
from pathlib import Path

from db.database import BASE_DIR, DB_PATH, get_connection


def import_data(data_dir=None, db_path=None):
    """Импортировать все данные одной транзакцией, не заменяя записи БД."""
    data_dir = Path(data_dir or BASE_DIR / "data")
    db_path = Path(db_path or DB_PATH)
    sources = {}
    for name in ("owners", "locations", "plants", "waterings"):
        with (data_dir / (name + ".json")).open(encoding="utf-8") as file:
            sources[name] = json.load(file)
        if not isinstance(sources[name], list):
            raise ValueError(f"{name}.json должен содержать список")
    schema = (BASE_DIR / "sql" / "schema.sql").read_text(encoding="utf-8")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection(db_path)
    try:
        conn.executescript(schema)
        with conn:
            for table in ("owners", "locations", "plants", "waterings"):
                exists = conn.execute("SELECT 1 FROM " + table + " LIMIT 1")
                if exists.fetchone():
                    raise ValueError(
                        "База уже содержит данные; импорт отменён."
                    )
            conn.executemany(
                "INSERT INTO owners VALUES (?, ?, ?)",
                [(x["id"], x["name"], x.get("email", ""))
                 for x in sources["owners"]],
            )
            conn.executemany(
                "INSERT INTO locations VALUES (?, ?, ?)",
                [(x["id"], x["name"], x["light"])
                 for x in sources["locations"]],
            )
            conn.executemany(
                "INSERT INTO plants VALUES (?, ?, ?, ?, ?, ?, ?)",
                [(x["id"], x["name"], x["species"], x["interval_days"],
                  x["last_watered"], x.get("owner_id"), x.get("location_id"))
                 for x in sources["plants"]],
            )
            conn.executemany(
                "INSERT INTO waterings VALUES (?, ?, ?, ?)",
                [(x["id"], x["plant_id"], x["watered_on"], x.get("note", ""))
                 for x in sources["waterings"]],
            )
        return {name: len(records) for name, records in sources.items()}
    finally:
        conn.close()


if __name__ == "__main__":
    counts = import_data()
    print("Импорт завершён:", counts)
