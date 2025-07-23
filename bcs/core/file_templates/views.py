"""
from .models import (
    Bean,
    Czapka,
    Czlonek,
    DawnyZarzad,
    HallOfFame,
    ImieSzlacheckie,
    InnaOsoba,
    WielkiMistrz,
    Zarzad,
    ZwierzeCzapkowe
)
from core.utils.autocompletion.AutocompletesGeneration import *

from core.models_dict import names as core
from encyklopedia.models_dict import names as encyklopedia
from kronika.models_dict import names as kronika

autocomplete_configs = [
    (Bean, ["staz"], [], [Czapka.__name__, Czlonek.__name__]),
    (
        Czlonek,
        ["rok_chrztu", "miesiac_chrztu", "dzien_chrztu", "status", "staz"],
        [],
        [
            Czapka.__name__,
            Czlonek.__name__
        ]
    ),
    (
        DawnyZarzad,
        [],
        [],
        [
            Czlonek.__name__,
            WielkiMistrz.__name__,
            kronika["CharakterystykaDzialanZarzadu"]
            kronika["Kadencja"],
        ]
    ),
    (HallOfFame, [], [], [Bean.__name__, Czlonek.__name__]),
    (ImieSzlacheckie, [], [], [Czlonek.__name__]),
    (InnaOsoba, ["kategoria"], [], [encyklopedia["Bractwo"]]),
    (WielkiMistrz, [], [], [Czlonek.__name__]),
    (
        Zarzad,
        [],
        [],
        [
            Czlonek.__name__,
            WielkiMistrz.__name__,
            kronika["CharakterystykaDzialanZarzadu"]
            kronika["Kadencja"],
        ]
    ),
    (ZwierzeCzapkowe, [], [], [Czlonek.__name__])
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
"""
