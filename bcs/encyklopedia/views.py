from .models import *
from core.utils.automation.ViewsGeneration import *

from kronika.models_dict import names as kronika

autocomplete_configs = [
    (
        Bractwo,
        ['panstwo', 'czapka', 'wiek_tradycje', 'rok_zalozenia'], [],
        []),
    (
        TradycjaBCS,
        ['autor_rodzaj', 'okolicznosci_powstania'], [],
        [kronika['Wydarzenie']]),
    (
        TradycjaInnegoBractwa,
        ['autor_rodzaj'], [],
        []),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
