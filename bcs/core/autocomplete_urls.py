from django.urls import path
from . import views
from .views import autocomplete_urls

app_name = "core_autocomplete"

urlpatterns = [
    path('custom-kadencja-autocomplete/', views.CustomKadencjaAutocomplete.as_view(), name='custom-kadencja-autocomplete'),
] + autocomplete_urls