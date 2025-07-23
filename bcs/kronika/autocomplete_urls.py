from django.urls import path
from . import custom_autocomplete_views
from .views import autocomplete_urls

app_name = "kronika_autocomplete"

# fields autocomplete
urlpatterns = [
    path(
        "custom-miejsce-from-wydarzenie-to-zdarzenie-autocomplete/",
        custom_autocomplete_views.CustomMiejsceFromWydarzenieToZdarzenieAutocomplete.as_view(),
        name="custom-miejsce-from-wydarzenie-to-zdarzenie-autocomplete",
    ),
] + autocomplete_urls
