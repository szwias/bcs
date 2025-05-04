from django.urls import path
from . import views

app_name = 'kronika'

# fields autocomplete
urlpatterns = [
    path('typ-miejsca-autocomplete/', views.TypMiejscaAutocomplete.as_view(), name='typ-miejsca-autocomplete'),
    path('typ-wydarzenia-autocomplete/', views.TypWydarzeniaAutocomplete.as_view(), name='typ-wydarzenia-autocomplete'),
    path('typ-wyjazdu-autocomplete/', views.TypWyjazduAutocomplete.as_view(), name='typ-wyjazdu-autocomplete'),
]

# records autocomplete
urlpatterns += [
    path('miejsce-autocomplete/', views.MiejsceAutocomplete.as_view(), name='miejsce-autocomplete'),
    path('zdarzenie-autocomplete/', views.ZdarzenieAutocomplete.as_view(), name='zdarzenie-autocomplete'),
]