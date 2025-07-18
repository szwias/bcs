from .models import *
from core.utils.automation.AutocompletesGeneration import *

from czapki.models_dict import names as czapki
from kronika.models_dict import names as kronika
from miejsca.models_dict import names as miejsca

autocomplete_configs = [
    (
        Bractwo,
        ['wiek_tradycje', 'rok_zalozenia'], [],
        [miejsca['Kraj'], GrupaBractw.__name__]),
    (
        GrupaBractw,
        [], [],
        [miejsca['Kraj'], czapki['RodzajCzapki']]),
    (
        Pojecie,
        ['origins'], [],
        [kronika['Wydarzenie']]),
    (
        Powiedzenie,
        [], [],
        []),
    (
        TradycjaBCS,
        ['okolicznosci_powstania'], [],
        [kronika['Wydarzenie'], GrupaBractw.__name__]),
    (
        TradycjaInnegoBractwa,
        [], [],
        [GrupaBractw.__name__]),
    (
        Zwyczaj,
        [], [],
        []),
    (
        Zrodlo,
        [], [],
        [])
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
