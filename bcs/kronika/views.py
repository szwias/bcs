
from .models import *
from core.utils.automation.ViewsGeneration import *

autocomplete_configs = [
    (Uczestnictwo,  [],         [],     ['czlonkowie.Czlonek']),
    (Miejsce,       ['typ'],    [],     []),
    (Zdarzenie,     [],         [],     ['Uczestnictwo']),
    (Wydarzenie,    ['typ'],    [],     ['Miejsce', 'Zdarzenie', 'Uczestnictwo']),
    (Proces,        [],         [],     ['Zdarzenie']),
    (Wyjazd,        ['typ'],    [],     ['Miejsce','Zdarzenie','Uczestnictwo']),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
# print(autocomplete_urls)
# print(f"{el}\n" for el in globals())
