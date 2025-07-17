from .models import *
from core.utils.automation.ViewsGeneration import *

from kronika.models_dict import names as kronika

autocomplete_configs = [
    (
        Bractwo,
        ['panstwo', 'czapka', 'wiek_tradycje', 'rok_zalozenia'], [],
        []),
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
        ['autor_rodzaj', 'okolicznosci_powstania'], [],
        [kronika['Wydarzenie']]),
    (
        TradycjaInnegoBractwa,
        ['autor_rodzaj'], [],
        []),
    (
        Zwyczaj,
        [], [],
        []),
    (
        Zrodlo,
        [], [],
        []),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
