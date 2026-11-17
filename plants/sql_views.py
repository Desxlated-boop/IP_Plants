"""Учебные страницы с данными из SQLite без использования Django ORM."""
from datetime import date
import sqlite3

from django.shortcuts import render

from db.database import get_connection
from db.queries import get_queries


def sql_pages(request, section="all"):
    """Показать каталог, журнал, поиск полива по дате и статистику."""
    value = request.GET.get("date", "")
    error = ""
    try:
        selected = date.fromisoformat(value) if value else date.today()
        if value and value != selected.isoformat():
            raise ValueError
    except ValueError:
        selected = None
        error = "Введите корректную дату в формате ГГГГ-ММ-ДД."
    queries = get_queries()
    try:
        conn = get_connection(read_only=True)
        try:
            def run(name, params=()):
                return conn.execute(queries[name], params).fetchall()

            context = {
                "plants": run("plants_list"),
                "waterings": run("watering_list"),
                "due": (
                    run("due_on_date", (selected.isoformat(),))
                    if selected else []
                ),
                "light_plants": run("plants_by_light", ("яркий",)),
                "watering_details": run("watering_details"),
                "plant_details": run("plant_details"),
                "plant_total": run("plant_total")[0]["total"],
                "watering_total": run("watering_total")[0]["total"],
                "by_owner": run("plants_by_owner"),
                "by_location": run("plants_by_location"),
                "by_watering": run("watering_by_plant", (1,)),
                "recent": run("recent_waterings", (3, 0)),
                "selected_date": selected.isoformat() if selected else value,
                "error": error,
                "section": section,
            }
        finally:
            conn.close()
    except sqlite3.Error:
        return render(request, "plants/sql_error.html", status=503)
    return render(request, "plants/sql_pages.html", context)
