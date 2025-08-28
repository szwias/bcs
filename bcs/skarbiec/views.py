from core.utils.autocompletion.AutocompletesGeneration import *
from .models import (
    Konto,
    Transakcja,
)

from osoby.models_dict import names as osoby

autocomplete_configs = [
    (Konto, [], [], [osoby["Byt"]]),
    (Transakcja, ["typ"], [], [Konto.__name__]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
