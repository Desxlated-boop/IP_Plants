"""Перенос коллекции из базы ПР7 в таблицы Django."""
from datetime import date
import sqlite3

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from db.database import DB_PATH
from locations.models import Location
from owners.models import Owner
from plants.models import Plant
from waterings.models import WateringLog


class Command(BaseCommand):
    help = "Перенести данные из базы ПР7 в пустые таблицы Django"

    def handle(self, *args, **options):
        if not DB_PATH.is_file():
            raise CommandError("База ПР7 не найдена: " + str(DB_PATH))
        models = (Owner, Location, Plant, WateringLog)
        if any(model.objects.exists() for model in models):
            raise CommandError("Таблицы Django не пусты; импорт отменён.")
        uri = DB_PATH.resolve().as_uri() + "?mode=ro"
        source = sqlite3.connect(uri, uri=True)
        source.row_factory = sqlite3.Row
        try:
            with transaction.atomic():
                for row in source.execute("SELECT * FROM owners ORDER BY id"):
                    Owner.objects.create(
                        id=row["id"], name=row["name"],
                        email=row["email"] or "",
                    )
                locations = source.execute(
                    "SELECT * FROM locations ORDER BY id"
                )
                for row in locations:
                    Location.objects.create(
                        id=row["id"], name=row["name"], light=row["light"]
                    )
                for row in source.execute("SELECT * FROM plants ORDER BY id"):
                    Plant.objects.create(
                        id=row["id"], name=row["name"], species=row["species"],
                        interval_days=row["interval_days"],
                        last_watered=date.fromisoformat(row["last_watered"]),
                        owner_id=row["owner_id"],
                        location_id=row["location_id"],
                    )
                waterings = source.execute(
                    "SELECT * FROM waterings ORDER BY id"
                )
                for row in waterings:
                    WateringLog.objects.create(
                        id=row["id"], plant_id=row["plant_id"],
                        watered_on=date.fromisoformat(row["watered_on"]),
                        note=row["note"] or "",
                    )
        finally:
            source.close()
        self.stdout.write(self.style.SUCCESS("Перенос данных завершён."))
