from .models import *
from core.utils.automation.AutocompletesGeneration import *

from czapki.models_dict import names as czapki
from czlonkowie.models_dict import names as czlonkowie
from kronika.models_dict import names as kronika
from miejsca.models_dict import names as miejsca

autocomplete_configs = [
    (
        Bractwo,
        ['wiek_tradycje', 'rok_zalozenia'], [],
        [miejsca['Kraj'], GrupaBractw.__name__, czlonkowie['Osoba']]),
    (
        GrupaBractw,
        [], [],
        [miejsca['Kraj'], czapki['RodzajCzapki']]),
    (
        Pojecie,
        ['origins'], [],
        [kronika['Wydarzenie'], czlonkowie['Osoba']]),
    (
        Powiedzenie,
        [], [],
        [czlonkowie['Osoba']]),
    (
        TradycjaBCS,
        ['okolicznosci_powstania', 'zapozyczona_czy_autorska'], [],
        [kronika['Wydarzenie'], GrupaBractw.__name__, czlonkowie['Osoba']]),
    (
        TradycjaInnegoBractwa,
        [], [],
        [GrupaBractw.__name__]),
    (
        Zwyczaj,
        [], [],
        [czlonkowie['Osoba']]),
    (
        Zrodlo,
        [], [],
        [czlonkowie['Osoba']])
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
