from .models import (
    Kadencja,
    PodsumowanieKadencji,
    TypWydarzeniaHistorycznego,
    WydarzenieHistoryczne,
    ZadanieChrzcielne,
)
from core.utils.autocompletion.AutocompletesGeneration import *

from encyklopedia.models_dict import names as encyklopedia
from kalendarz.models_dict import names as kalendarz
from osoby.models_dict import names as osoby
from zrodla.models_dict import names as zrodla

autocomplete_configs = [
    (
        PodsumowanieKadencji,
        [],
        [],
        [osoby["Czlonek"], osoby["Zarzad"]],
    ),
    (
        Kadencja,
        [],
        [],
        [Kadencja.__name__, WydarzenieHistoryczne.__name__, osoby["Zarzad"]],
    ),
    (TypWydarzeniaHistorycznego, [], [], []),
    (
        WydarzenieHistoryczne,
        [],
        [],
        [
            TypWydarzeniaHistorycznego.__name__,
            encyklopedia["Pojecie"],
            kalendarz["WydarzenieKalendarzowe"],
            zrodla["Dokument"],
        ]),
    (ZadanieChrzcielne, [], [], [osoby["Czlonek"]]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
