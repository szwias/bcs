from core.utils.autocompletion.AutocompletesGeneration import *
from .models import (
    Nagrodzeni,
    Odznaczenie,
)

from osoby.models_dict import names as osoby
from zrodla.models_dict import names as zrodla

autocomplete_configs = [
    (Nagrodzeni, [], [], [Odznaczenie.__name__, osoby["Byt"]]),
    (Odznaczenie, ["rok_powstania"], [], [osoby["Byt"], zrodla["Dokument"]])
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
