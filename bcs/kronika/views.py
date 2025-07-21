from .models import *
from core.utils.autocompletion.AutocompletesGeneration import *

from osoby.models_dict import names as osoby
from miejsca.models_dict import names as miejsca

autocomplete_configs = [
    (
        CharakterystykaDzialanZarzadu,
        [], [],
        [
            osoby['Czlonek'], osoby['DawnyZarzad'], osoby['Zarzad']]),
    (
        ObrazWydarzenie,
        [], [],
        [
            Wydarzenie.__name__,
            osoby['Osoba']
        ]),
    (
        ObrazZdarzenie,
        [], [],
        [
            Zdarzenie.__name__,
            miejsca['Miejsce'], osoby['Osoba']
        ]),
    (
        Proces,
        [], [],
        [
            Zdarzenie.__name__,
        ]),
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
        [
            TypWydarzenia.__name__, TypWyjazdu.__name__, Zdarzenie.__name__,
            miejsca['Miejsce' ], osoby['Osoba'],
        ]),
    (
        Zdarzenie,
        [], [],
        [
            ObrazZdarzenie.__name__, Wydarzenie.__name__,
            osoby['Osoba']
        ]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
