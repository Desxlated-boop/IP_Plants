"""ASGI-конфигурация проекта Plantly."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plantly.settings")

application = get_asgi_application()
