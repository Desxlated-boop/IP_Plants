"""Загрузка данных проекта для веб-представлений."""
from django.conf import settings

from storage import Dataset, load_all


def load_data() -> Dataset:
    """Загрузить владельцев, места, растения и журнал из data/."""
    return load_all(str(settings.BASE_DIR / "data"))
