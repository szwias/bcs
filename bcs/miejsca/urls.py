from django.urls import path

from . import views

app_name = "miejsca"

urlpatterns = [
    path("mapa/", views.mapa, name="mapa"),
    path("mapa/dane/", views.mapa_dane, name="mapa_dane"),
]
