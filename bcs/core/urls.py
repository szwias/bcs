from django.urls import path
from .views import autocomplete_urls
from . import views

app_name = 'core'

urlpatterns = [
    path('custom-kadencja-autocomplete/', views.CustomKadencjaAutocomplete.as_view(), name='custom-kadencja-autocomplete'),
] + autocomplete_urls