"""Подключение к отдельной базе коллекции растений."""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "plants.sqlite"


def get_connection(path=DB_PATH, read_only=False):
    """Открыть базу, включив доступ к полям по имени и внешние ключи."""
    if read_only:
        uri = Path(path).resolve().as_uri() + "?mode=ro"
        connection = sqlite3.connect(uri, uri=True)
    else:
        connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
