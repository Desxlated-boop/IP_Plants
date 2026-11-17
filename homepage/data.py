"""Загрузка данных для веб-представлений через Django ORM."""
from locations.models import Location
from owners.models import Owner
from plants.models import Plant
from waterings.models import WateringLog


def load_data():
    """Получить коллекцию и связанные объекты из базы Django."""
    return (
        Owner.objects.all(),
        Location.objects.all(),
        Plant.objects.select_related("owner", "location"),
        WateringLog.objects.select_related(
            "plant", "plant__owner", "plant__location"
        ),
    )
