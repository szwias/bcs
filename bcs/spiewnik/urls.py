from django.urls import path
from . import views

app_name = "spiewnik"

urlpatterns = [
    path("piosenka/<int:pk>/", views.piosenka, name="piosenka"),
]
