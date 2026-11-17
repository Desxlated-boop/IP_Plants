"""Загрузка именованных SQL-запросов из файла проекта."""
from db.database import BASE_DIR


def get_queries():
    """Вернуть словарь: имя запроса и его SQL-текст."""
    source = (BASE_DIR / "sql" / "queries.sql").read_text(encoding="utf-8")
    queries = {}
    for section in source.split("-- name: ")[1:]:
        name, sql = section.split("\n", 1)
        queries[name.strip()] = sql.strip()
    return queries
