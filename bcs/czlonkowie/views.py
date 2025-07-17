from .models import Bean, Czapka, Czlonek, DawnyZarzad, HallOfFame, ImieSzlacheckie, InnaOsoba, WielkiMistrz, \
    Zarzad, ZwierzeCzapkowe, Osoby
from core.utils.automation.ViewsGeneration import *

from core.models_dict import names as core

autocomplete_configs = [
    (
        Bean,
        ['staz'], [],
        [Czapka.__name__, Czlonek.__name__]),
    (
        Czlonek,
        ['rok_chrztu', 'miesiac_chrztu', 'dzien_chrztu', 'status', 'staz'], [],
        [Czapka.__name__, Czlonek.__name__]),
    (
        DawnyZarzad,
        [], [],
        [Czlonek.__name__, core['Kadencja']]),
    (
        HallOfFame,
        [], [],
        [Czlonek.__name__, Bean.__name__]),
    (
        ImieSzlacheckie,
        [], [],
        [Czlonek.__name__]),
    (
        InnaOsoba,
        ['kategoria'], [],
        []),
    (
        Osoby,
        [], [],
        []),
    (
        WielkiMistrz,
        [], [],
        []),
    (
        Zarzad,
        [], [],
        [Czlonek.__name__, core['Kadencja']]),
    (
        ZwierzeCzapkowe,
        [], [],
        [Czlonek.__name__]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
