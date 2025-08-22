from django.urls import path
from kalendarz import custom_autocomplete_views
from .views import autocomplete_urls

app_name = "kalendarz_autocomplete"

# fields autocomplete
urlpatterns = [
    path(
        "custom-miejsce-from-wydarzenie-to-zdarzenie-autocomplete/",
        custom_autocomplete_views.CustomMiejsceFromWydarzenieKalendarzoweToZdarzenieAutocomplete.as_view(),
        name="custom-miejsce-from-wydarzenie-to-zdarzenie-autocomplete",
    ),
] + autocomplete_urls
