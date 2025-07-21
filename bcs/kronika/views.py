from .models import *
from core.utils.automation.AutocompletesGeneration import *

from osoby.models_dict import names as osoby
from miejsca.models_dict import names as miejsca

autocomplete_configs = [
    (
        CharakterystykaDzialanZarzadu,
        [], [],
        [osoby['Zarzad'], osoby['DawnyZarzad'], osoby['Czlonek']]),
    (
        ObrazWydarzenie,
        [], [],
        [Wydarzenie.__name__, osoby['Osoba']]),
    (
        ObrazZdarzenie,
        [], [],
        [Zdarzenie.__name__, miejsca['Miejsce'], osoby['Osoba']]),
    (
        Proces,
        [], [],
        [Zdarzenie.__name__]),
    (
        TypWydarzenia,
        [], [],
        []),
    (
        TypWyjazdu,
        [], [],
        []),
    (
        Wydarzenie,
        ['typ_wydarzenia', 'typ_wyjazdu', 'czy_to_wyjazd'], [],
        [miejsca['Miejsce' ], Zdarzenie.__name__, osoby['Osoba']]),
    (
        Zdarzenie,
        [], [],
        [ObrazZdarzenie.__name__, Wydarzenie.__name__, osoby['Osoba']]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
