from .models import *
from core.utils.automation.ViewsGeneration import *

autocomplete_configs = [
    (TradycjaBCS, ['autor_rodzaj', 'okolicznosci_powstania'], [], ['kronika.Wydarzenie', 'kronika.Wyjazd', 'czlonkowie.Czlonek']),
    (TradycjaInnegoBractwa, ['autor_rodzaj'], [], [])
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
