"""Корневая маршрутизация проекта Plantly."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("plants/", include("plants.urls")),
    path("owners/", include("owners.urls")),
    path("locations/", include("locations.urls")),
    path("waterings/", include("waterings.urls")),
]

handler404 = "homepage.views.page_not_found"
