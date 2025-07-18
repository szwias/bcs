from .models import *
from core.utils.automation.AutocompletesGeneration import *

from czlonkowie.models_dict import names as czlonkowie
from miejsca.models_dict import names as miejsca

autocomplete_configs = [
    (
        CharakterystykaDzialanZarzadu,
        [], [],
        [czlonkowie['Zarzad'], czlonkowie['DawnyZarzad'], czlonkowie['OldCzlonek']]),
    (
        ObrazWydarzenie,
        [], [],
        [Wydarzenie.__name__]),
    (
        ObrazZdarzenie,
        [], [],
        [Zdarzenie.__name__, miejsca['Miejsce']]),
    (
        Proces,
        [], [],
        [Zdarzenie.__name__]),
    (
        Wydarzenie,
        ['typ_wydarzenia', 'typ_wyjazdu', 'czy_to_wyjazd'], [],
        [miejsca['Miejsce' ], Zdarzenie.__name__]),
    (
        Zdarzenie,
        [], [],
        [ObrazZdarzenie.__name__, Wydarzenie.__name__]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
