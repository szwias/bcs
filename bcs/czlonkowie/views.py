from .models import Czlonek
from core.utils.automation.ViewsGeneration import setup_autocompletes

autocomplete_configs = [
    (Czlonek, ['rok_chrztu', 'miesiac_chrztu', 'dzien_chrztu', 'status', 'staz'], [], ['Czapka', 'Czlonek']),
]

setup_autocompletes(autocomplete_configs, globals())
