# czlonkowie/urls.py
from django.urls import path
from .views import *
from .views import autocomplete_urls

app_name = 'czlonkowie'

urlpatterns = [] + autocomplete_urls
# fields autocomplete
# urlpatterns = [
#     path('czlonek-rok-chrztu-by-label-autocomplete/', RokChrztuAutocomplete.as_view(), name='czlonek-rok-chrztu-by-label-autocomplete'),
#     path('czlonek-miesiac-chrztu-by-label-autocomplete/', MiesiacChrztuAutocomplete.as_view(), name='czlonek-miesiac-chrztu-by-label-autocomplete'),
#     path('czlonek-dzien-chrztu-by-label-autocomplete/', DzienChrztuAutocomplete.as_view(), name='czlonek-dzien-chrztu-by-label-autocomplete'),
#     path('czlonek-staz-by-label-autocomplete/', StazAutocomplete.as_view(), name='czlonek-staz-by-label-autocomplete'),
#     path('czlonek-status-by-label-autocomplete/', StatusAutocomplete.as_view(), name='czlonek-status-by-label-autocomplete'),
# ]
#
# # models autocomplete
# urlpatterns += [
#     path('czlonek-records-autocomplete/', CzlonekAutocomplete.as_view(), name='czlonek-records-autocomplete'),
#     path('czapka-records-autocomplete/', CzapkaAutocomplete.as_view(), name='czapka-records-autocomplete'),
# ]
# pattern_paths = {p.pattern._route for p in urlpatterns}
# autocomplete_paths = {p.pattern._route for p in autocomplete_urls}
#
# print(pattern_paths == autocomplete_paths) # True
