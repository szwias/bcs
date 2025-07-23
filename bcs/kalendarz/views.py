from .models import *
from core.utils.autocompletion.AutocompletesGeneration import *
from miejsca.models_dict import names as miejsca
from osoby.models_dict import names as osoby

autocomplete_configs = [
    (ObrazWydarzenie, [], [], [Wydarzenie.__name__, osoby["Osoba"]]),
    (
        ObrazZdarzenie,
        [],
        [],
        [Zdarzenie.__name__, miejsca["Miejsce"], osoby["Osoba"]],
    ),
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
        [ObrazZdarzenie.__name__, Wydarzenie.__name__, osoby["Osoba"]],
    ),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
