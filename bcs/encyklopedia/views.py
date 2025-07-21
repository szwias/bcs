from .models import *
from core.utils.automation.AutocompletesGeneration import *

from czapki.models_dict import names as czapki
from osoby.models_dict import names as osoby
from kronika.models_dict import names as kronika
from miejsca.models_dict import names as miejsca

autocomplete_configs = [
    (
        Bractwo,
        ['wiek_tradycje', 'rok_zalozenia'], [],
        [miejsca['Kraj'], GrupaBractw.__name__, osoby['Osoba']]),
    (
        GrupaBractw,
        [], [],
        [miejsca['Kraj'], czapki['RodzajCzapki']]),
    (
        Pojecie,
        ['origins'], [],
        [kronika['Wydarzenie'], osoby['Osoba']]),
    (
        Powiedzenie,
        [], [],
        [osoby['Osoba']]),
    (
        TradycjaBCS,
        ['okolicznosci_powstania', 'zapozyczona_czy_autorska'], [],
        [kronika['Wydarzenie'], GrupaBractw.__name__, osoby['Osoba']]),
    (
        TradycjaInnegoBractwa,
        [], [],
        [GrupaBractw.__name__]),
    (
        Zwyczaj,
        [], [],
        [osoby['Osoba']]),
    (
        Zrodlo,
        [], [],
        [osoby['Osoba']])
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
