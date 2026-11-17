"""Общие сведения о коллекции для шаблонов."""
from plants.models import Plant


def collection_summary(request):
    return {"collection_plant_count": Plant.objects.count()}
