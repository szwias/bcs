from django.urls import path
from . import views

app_name = 'core'

# fields autocomplete
urlpatterns = [
    path('rozpoczecie-autocomplete/', views.RozpoczecieAutocomplete.as_view(), name='rozpoczecie-autocomplete'),
]

# records autocomplete
urlpatterns += [
    path('kadencja-autocomplete/', views.KadencjaAutocomplete.as_view(), name='kadencja-autocomplete'),
]