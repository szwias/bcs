from .models import (
    CharakterystykaDzialanZarzadu,
    Kadencja,
    TypWydarzeniaHistorycznego,
    WydarzenieHistoryczne,
)
from core.utils.autocompletion.AutocompletesGeneration import *

from kronika.models_dict import names as kronika
from osoby.models_dict import names as osoby

autocomplete_configs = [
    (
        CharakterystykaDzialanZarzadu,
        [],
        [],
        [osoby["Czlonek"], osoby["DawnyZarzad"], osoby["NowyZarzad"]],
    ),
    (
        Kadencja,
        [],
        [],
        [
            WydarzenieHistoryczne.__name__,
            kronika["Kadencja"],
            osoby["NowyZarzad"]],
    ),
    (TypWydarzeniaHistorycznego, [], [], []),
    (WydarzenieHistoryczne, [], [], [TypWydarzeniaHistorycznego.__name__]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
