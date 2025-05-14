
from .models import *
from core.utils.automation.ViewsGeneration import *

autocomplete_configs = [
    (Miejsce,           ['typ'],                                [],     []),
    (Zdarzenie,         [],                                     [],     ['czlonkowie.Osoby']),
    (ObrazZdarzenie,    [],                                     [],     ['Zdarzenie', 'Miejsce', 'czlonkowie.Osoby']),
    (Wydarzenie,        ['typ_wydarzenia', 'typ_wyjazdu'],      [],     ['Miejsce', 'Zdarzenie', 'czlonkowie.Osoby']),
    (ObrazWydarzenie,   [],                                     [],     ['Wydarzenie', 'czlonkowie.Osoby']),
    (Proces,            [],                                     [],     ['Zdarzenie']),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
