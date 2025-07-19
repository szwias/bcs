from .models import *
from core.utils.automation.AutocompletesGeneration import *

from czlonkowie.models_dict import names as czlonkowie
from miejsca.models_dict import names as miejsca

autocomplete_configs = [
    (
        CharakterystykaDzialanZarzadu,
        [], [],
        [czlonkowie['Zarzad'], czlonkowie['DawnyZarzad'], czlonkowie['Czlonek']]),
    (
        ObrazWydarzenie,
        [], [],
        [Wydarzenie.__name__, czlonkowie['Osoba']]),
    (
        ObrazZdarzenie,
        [], [],
        [Zdarzenie.__name__, miejsca['Miejsce'], czlonkowie['Osoba']]),
    (
        Proces,
        [], [],
        [Zdarzenie.__name__]),
    (
        Wydarzenie,
        ['typ_wydarzenia', 'typ_wyjazdu', 'czy_to_wyjazd'], [],
        [miejsca['Miejsce' ], Zdarzenie.__name__, czlonkowie['Osoba']]),
    (
        Zdarzenie,
        [], [],
        [ObrazZdarzenie.__name__, Wydarzenie.__name__, czlonkowie['Osoba']]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
