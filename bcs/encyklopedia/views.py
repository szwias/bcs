from .models import *
from core.utils.automation.ViewsGeneration import *

autocomplete_configs = [
    (Tradycja, ['okolicznosci_powstania'], [], ['kronika.Wydarzenie', 'kronika.Wyjazd']),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
