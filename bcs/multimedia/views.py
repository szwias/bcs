from core.utils.autocompletion.AutocompletesGeneration import *
from .models import ObrazWydarzenie, ObrazZdarzenie

from kalendarz.models_dict import names as kalendarz
from miejsca.models_dict import names as miejsca
from osoby.models_dict import names as osoby

autocomplete_configs = [
    (ObrazWydarzenie, [], [], [kalendarz["Wydarzenie"], osoby["Osoba"]]),
    (
        ObrazZdarzenie,
        [],
        [],
        [kalendarz["Zdarzenie"], miejsca["Miejsce"], osoby["Osoba"]],
    ),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
