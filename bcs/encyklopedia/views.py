from .models import *
from core.utils.automation.ViewsGeneration import *

autocomplete_configs = [
    (Bractwo, ['panstwo', 'czapka', 'wiek_tradycje', 'rok_zalozenia'], [], []),
    (TradycjaBCS, ['autor_rodzaj', 'okolicznosci_powstania'], [], ['kronika.Wydarzenie', 'czlonkowie.Czlonek']),
    (TradycjaInnegoBractwa, ['autor_rodzaj'], [], []),
    (Zwyczaj, [], [], ['czlonkowie.Osoby']),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
