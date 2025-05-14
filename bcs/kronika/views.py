
from .models import *
from core.utils.automation.ViewsGeneration import *

autocomplete_configs = [
    (Miejsce,           ['typ'],    [],     []),
    (Zdarzenie,         [],         [],     ['czlonkowie.Osoby']),
    (Wydarzenie,        ['typ'],    [],     ['Miejsce', 'czlonkowie.Osoby']),
    (ObrazWydarzenie,   [],         [],     ['Wydarzenie', 'czlonkowie.Osoby']),
    (Proces,            [],         [],     ['Zdarzenie']),
    (Wyjazd,            ['typ'],    [],     ['Miejsce', 'Zdarzenie', 'czlonkowie.Osoby']),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
