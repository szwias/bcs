from .models_imports import *
from core.utils.autocompletion.AutocompletesGeneration import *

from zrodla.models_dict import names as zrodla

autocomplete_configs = [
    (DlugoscKadencji, [], [], []),
    (Podmiot, [], [], [DlugoscKadencji.__name__]),
    (
        PrawoObowiazek,
        [],
        [],
        [Podmiot.__name__, RelacjaPrawna.__name__, zrodla["Dokument"]]
     ),
    (
        RelacjaPrawna,
        [],
        ["prawo_czy_obowiazek"],
        [],
    ),
    (
        Struktura,
        [],
        [],
        [
            DlugoscKadencji.__name__,
            WielkoscStruktury.__name__
        ]
    ),
    (Rola, [], [], [DlugoscKadencji.__name__]),
    (WielkoscStruktury, [], [], []),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
