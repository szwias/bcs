from .models import (
    DlugoscKadencji,
    Podmiot,
    PrawoObowiazek,
    RelacjaPrawna,
    Rola,
    Struktura,
    WielkoscStruktury,
)
from core.utils.autocompletion.AutocompletesGeneration import *

from zrodla.models_dict import names as zrodla

autocomplete_configs = [
    (Podmiot, [], [], []),
    (DlugoscKadencji, [], [], []),
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
    (Struktura, [], [], []),
    (Rola, [], [], []),
    (WielkoscStruktury, [], [], []),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
