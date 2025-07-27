from .models import (
    PodsumowanieKadencji,
    Kadencja,
    TypWydarzeniaHistorycznego,
    WydarzenieHistoryczne,
)
from core.utils.autocompletion.AutocompletesGeneration import *

from osoby.models_dict import names as osoby

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
    (WydarzenieHistoryczne, [], [], [TypWydarzeniaHistorycznego.__name__]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
