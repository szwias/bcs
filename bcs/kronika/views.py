
from .models import *
from core.utils.automation.ViewsGeneration import *

autocomplete_configs = [
    (Miejsce,           ['typ'],    [],     []),
    (Zdarzenie,         [],         [],     ['Uczestnictwo']),
    (Wydarzenie,        ['typ'],    [],     ['Miejsce', 'Uczestnictwo']),
    (ObrazWydarzenie,   [],         [],     ['Wydarzenie', 'czlonkowie.Czlonek', 'czlonkowie.InnaOsoba']),
    (Proces,            [],         [],     ['Zdarzenie']),
    (Wyjazd,            ['typ'],    [],     ['Miejsce','Zdarzenie','Uczestnictwo']),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
