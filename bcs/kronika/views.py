
from .models import *
from core.utils.automation.ViewsGeneration import *

autocomplete_configs = [
    (Miejsce,           ['typ'],    [],     []),
    (Zdarzenie,         [],         [],     ['Osoby']),
    (Wydarzenie,        ['typ'],    [],     ['Miejsce', 'Osoby']),
    (ObrazWydarzenie,   [],         [],     ['Wydarzenie', 'Osoby']),
    (Proces,            [],         [],     ['Zdarzenie']),
    (Wyjazd,            ['typ'],    [],     ['Miejsce', 'Zdarzenie', 'Osoby']),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
