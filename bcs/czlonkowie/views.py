from .models import Czlonek
from core.utils.automation.ViewsGeneration import *

autocomplete_configs = [
    (Czlonek, ['rok_chrztu', 'miesiac_chrztu', 'dzien_chrztu', 'status', 'staz'], [], ['Czapka', 'Czlonek']),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
