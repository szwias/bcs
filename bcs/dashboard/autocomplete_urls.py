from django.urls import path

from .autocomplete_views import (
    autocomplete_urls,
    CustomAppDjangoUrlAutocomplete,
)

app_name = "dashboard_autocomplete"

urlpatterns = [
    path(
        "custom-app-django-url-autocomplete/",
        CustomAppDjangoUrlAutocomplete.as_view(),
        name="custom-app-django-url-autocomplete",
    ),
] + autocomplete_urls
