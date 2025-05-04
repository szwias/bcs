# czlonkowie/urls.py
from django.urls import path
from .views import *
# from .views import autocomplete_urls

app_name = 'czlonkowie'

# fields autocomplete
urlpatterns = [
    path('rok-chrztu-autocomplete/', RokChrztuAutocomplete.as_view(), name='rok-chrztu-autocomplete'),
    path('miesiac-chrztu-autocomplete/', MiesiacChrztuAutocomplete.as_view(), name='miesiac-chrztu-autocomplete'),
    path('dzien-chrztu-autocomplete/', DzienChrztuAutocomplete.as_view(), name='dzien-chrztu-autocomplete'),
    path('staz-autocomplete/', StazAutocomplete.as_view(), name='staz-autocomplete'),
    path('status-autocomplete/', StatusAutocomplete.as_view(), name='status-autocomplete'),
]

# models autocomplete
urlpatterns += [
    path('czlonek-autocomplete/', CzlonekAutocomplete.as_view(), name='czlonek-autocomplete'),
    path('czapka-autocomplete/', CzapkaAutocomplete.as_view(), name='czapka-autocomplete'),
]