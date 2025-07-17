from .models import *
from core.utils.automation.ViewsGeneration import *

from czlonkowie.models_dict import names as czlonkowie
from kronika.models_dict import names as kronika

autocomplete_configs = [
    (
        Bractwo,
        ['panstwo', 'czapka', 'wiek_tradycje', 'rok_zalozenia'], [],
        []),
    (
        Powiedzenie,
        [], [],
        [czlonkowie['Czlonek']]),
    (
        TradycjaBCS,
        ['autor_rodzaj', 'okolicznosci_powstania'], [],
        [kronika['Wydarzenie'], czlonkowie['Czlonek']]),
    (
        TradycjaInnegoBractwa,
        ['autor_rodzaj'], [],
        []),
    (
        Zwyczaj,
        [], [],
        []),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
