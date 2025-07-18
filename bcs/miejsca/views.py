from core.utils.automation.AutocompletesGeneration import *
from .models import Kraj, Miejsce, TypMiejsca, Uczelnia, Wydzial

autocomplete_configs = [
    (
        Miejsce,
        [], [],
        [TypMiejsca.__name__]
    ),
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
