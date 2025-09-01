from django.urls import path
from .views import search

app_name = "wyszukiwarka"

urlpatterns = [
    path("search/", search, name="search"),
]
