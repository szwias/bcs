from core.utils.automation.AutocompletesGeneration import *
from .models import Kraj, Uczelnia, Wydzial

autocomplete_configs = [
    (
        Uczelnia,
        [], [],
        [Kraj.__name__]
    ),
    (
        Wydzial,
        [], [],
        [Uczelnia.__name__]
    ),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
