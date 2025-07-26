from django.db.models import CharField
from django.db.models.functions import Cast

from .models import (
    CharakterystykaDzialanZarzadu,
    Kadencja,
    TypWydarzeniaHistorycznego,
    WydarzenieHistoryczne,
)
from core.utils.autocompletion.AutocompletesGeneration import *

from kalendarz.models_dict import names as kalendarz
from osoby.models_dict import names as osoby

autocomplete_configs = [
    (
        CharakterystykaDzialanZarzadu,
        [],
        [],
        [osoby["Czlonek"], osoby["DawnyZarzad"], osoby["Zarzad"]],
    ),
    (
        Kadencja,
        [],
        ["lata"],
        [WydarzenieHistoryczne.__name__, osoby["Zarzad"]],
    ),
    (TypWydarzeniaHistorycznego, [], [], []),
    (WydarzenieHistoryczne, [], [], [TypWydarzeniaHistorycznego.__name__]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
