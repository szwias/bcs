from multimedia.models import ObrazZdarzenie, ObrazWydarzenie
from .models import *
from core.utils.autocompletion.AutocompletesGeneration import *

from miejsca.models_dict import names as miejsca
from multimedia.models_dict import names as multimedia
from osoby.models_dict import names as osoby

autocomplete_configs = [
    (TypWydarzenia, [], [], []),
    (TypWyjazdu, [], [], []),
    (
        Wydarzenie,
        ["typ_wydarzenia", "typ_wyjazdu"],
        [],
        [
            TypWydarzenia.__name__,
            TypWyjazdu.__name__,
            Zdarzenie.__name__,
            miejsca["Miejsce"],
            osoby["Osoba"],
        ],
    ),
    (
        Zdarzenie,
        [],
        [],
        [Wydarzenie.__name__, multimedia["ObrazZdarzenie"], osoby["Osoba"]],
    ),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
