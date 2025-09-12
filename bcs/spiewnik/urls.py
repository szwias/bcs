from django.urls import path

from . import views

app_name = "spiewnik"

urlpatterns = [
    path("spis_tresci/", views.spis_tresci, name="spis_tresci"),
    path("piosenka/<int:pk>/", views.piosenka, name="piosenka"),
]
