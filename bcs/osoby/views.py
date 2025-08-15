from .models import (
    Bean,
    Czlonek,
    DawnyZarzad,
    HallOfFame,
    ImieSzlacheckie,
    InnaOsoba,
    KomisjaRewizyjna,
    Osoba,
    WielkiMistrz,
    NowyZarzad,
    ZwierzeCzapkowe,
)
from core.utils.autocompletion.AutocompletesGeneration import *

from czapki.models_dict import names as czapki
from encyklopedia.models_dict import names as encyklopedia
from kalendarz.models_dict import names as kalendarz
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
            kalendarz["Wydarzenie"],
        ],
    ),
    (
        DawnyZarzad,
        [],
        [],
        [
            Czlonek.__name__,
            WielkiMistrz.__name__,
            kronika["PodsumowanieKadencji"],
            kronika["Kadencja"],
        ],
    ),
    (HallOfFame, [], [], [Osoba.__name__]),
    (ImieSzlacheckie, [], [], [Czlonek.__name__]),
    (InnaOsoba, ["kategoria"], [], [encyklopedia["Bractwo"]]),
    (KomisjaRewizyjna, [], [], [Osoba.__name__, kronika["Kadencja"]]),
    (
        NowyZarzad,
        [],
        [],
        [
            Czlonek.__name__,
            WielkiMistrz.__name__,
            kronika["PodsumowanieKadencji"],
            kronika["Kadencja"],
        ],
    ),
    (Osoba, [], [], []),
    (WielkiMistrz, [], [], [Czlonek.__name__]),
    (ZwierzeCzapkowe, [], [], [Czlonek.__name__]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
