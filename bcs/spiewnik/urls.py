from django.urls import path

from . import views

app_name = "spiewnik"

urlpatterns = [
    path("spis_tresci/", views.spis_tresci, name="spis_tresci"),
    path(
        "spis_tresci_kat/<int:category_pk>/",
        views.spis_tresci_kat,
        name="spis_tresci_kat",
    ),
    path(
        "piosenka/<int:category_pk>/<int:pk>/", views.piosenka, name="piosenka"
    ),
]
