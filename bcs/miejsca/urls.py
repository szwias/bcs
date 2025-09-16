from django.urls import path

from . import views

app_name = "miejsca"

urlpatterns = [
    path("map/", views.miejsca_map, name="miejsca_map"),
    path("map/data/", views.miejsca_map_data, name="miejsca_map_data"),
]
