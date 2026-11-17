"""Маршруты приложения plants."""
from django.urls import path

from . import views
from . import sql_views
from . import orm_views

app_name = "plants"

urlpatterns = [
    path("", views.plant_list, name="list"),
    path("database/", sql_views.sql_pages, name="database"),
    path("statistics/", orm_views.statistics, name="statistics"),
    path("database/plants/", sql_views.sql_pages, {"section": "catalog"},
         name="database_plants"),
    path("database/waterings/", sql_views.sql_pages, {"section": "journal"},
         name="database_waterings"),
    path("database/search/", sql_views.sql_pages, {"section": "search"},
         name="database_search"),
    path("database/statistics/", sql_views.sql_pages, {"section": "stats"},
         name="database_stats"),
    path("thirsty/", views.plants_thirsty, name="thirsty"),
    path("p/<slug:slug>/", views.plant_detail_slug, name="detail_slug"),
    path("<int:plant_id>/", views.plant_detail, name="detail"),
]
