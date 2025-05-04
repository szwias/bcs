# czlonkowie/urls.py
from django.urls import path
from .views import *
# from .views import autocomplete_urls

app_name = 'czlonkowie'

# fields autocomplete
urlpatterns = [
    path('rok-chrztu-autocomplete/', RokChrztuAutocomplete.as_view(), name='czlonek_rok_chrztu_label_autocomplete'),
    path('miesiac-chrztu-autocomplete/', MiesiacChrztuAutocomplete.as_view(), name='czlonek_miesiac_chrztu_label_autocomplete'),
    path('dzien-chrztu-autocomplete/', DzienChrztuAutocomplete.as_view(), name='czlonek_dzien_chrztu_label_autocomplete'),
    path('staz-autocomplete/', StazAutocomplete.as_view(), name='czlonek_staz_label_autocomplete'),
    path('status-autocomplete/', StatusAutocomplete.as_view(), name='czlonek_status_label_autocomplete'),
]

# models autocomplete
urlpatterns += [
    path('czlonek-autocomplete/', CzlonekAutocomplete.as_view(), name='czlonek_records_autocomplete'),
    path('czapka-autocomplete/', CzapkaAutocomplete.as_view(), name='czapka_records_autocomplete'),
]