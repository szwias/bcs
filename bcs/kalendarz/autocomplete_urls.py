from django.urls import path

from .autocomplete_views import (
    autocomplete_urls,
    CustomMiejsceFromWydarzenieKalendarzoweToZdarzenieAutocomplete,
)

app_name = "kalendarz_autocomplete"

# fields autocomplete
urlpatterns = [
    path(
        "custom-miejsce-from-wydarzenie-to-zdarzenie-autocomplete/",
        CustomMiejsceFromWydarzenieKalendarzoweToZdarzenieAutocomplete.as_view(),
        name="custom-miejsce-from-wydarzenie-to-zdarzenie-autocomplete",
    ),
] + autocomplete_urls
