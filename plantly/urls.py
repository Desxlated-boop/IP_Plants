"""Корневая маршрутизация проекта Plantly."""
from django.contrib import admin
from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("plants/", include("plants.urls")),
    path("owners/", include("owners.urls")),
    path("locations/", include("locations.urls")),
    path("waterings/", include("waterings.urls")),
]

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))

handler404 = "homepage.views.page_not_found"
