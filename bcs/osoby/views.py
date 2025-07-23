from .models import (
    Bean,
    Czlonek,
    InnaOsoba,
    Osoba,
    DawnyZarzad,
    HallOfFame,
    ImieSzlacheckie,
    WielkiMistrz,
    Zarzad,
    ZwierzeCzapkowe,
)
from core.utils.autocompletion.AutocompletesGeneration import *

from core.models_dict import names as core
from czapki.models_dict import names as czapki
from encyklopedia.models_dict import names as encyklopedia
from kronika.models_dict import names as kronika

autocomplete_configs = [
    (Bean, ["staz"], [], [Czlonek.__name__, czapki["Czapka"]]),
    (
        Czlonek,
        ["rok_chrztu", "miesiac_chrztu", "dzien_chrztu", "status", "staz"],
        [],
        [
            Czlonek.__name__,
            czapki["Czapka"],
        ],
    ),
    (
        DawnyZarzad,
        [],
        [],
        [
            Czlonek.__name__,
            WielkiMistrz.__name__,
            core["Kadencja"],
            kronika["CharakterystykaDzialanZarzadu"],
        ],
    ),
    (HallOfFame, [], [], [Bean.__name__, Czlonek.__name__]),
    (ImieSzlacheckie, [], [], [Czlonek.__name__]),
    (InnaOsoba, ["kategoria"], [], [encyklopedia["Bractwo"]]),
    (Osoba, [], [], []),
    (WielkiMistrz, [], [], [Czlonek.__name__]),
    (
        Zarzad,
        [],
        [],
        [
            Czlonek.__name__,
            WielkiMistrz.__name__,
            core["Kadencja"],
            kronika["CharakterystykaDzialanZarzadu"],
        ],
    ),
    (ZwierzeCzapkowe, [], [], [Czlonek.__name__])
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
