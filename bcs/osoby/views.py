from .model_imports import *
from core.utils.autocompletion.AutocompletesGeneration import *

from czapki.models_dict import names as czapki
from encyklopedia.models_dict import names as encyklopedia
from kalendarz.models_dict import names as kalendarz
from kronika.models_dict import names as kronika
from miejsca.models_dict import names as miejsca
from zrodla.models_dict import names as zrodla

autocomplete_configs = [
    (Bean, ["staz"], [], [Czlonek.__name__, czapki["Czapka"]]),
    (
        Bractwo,
        ["rok_zalozenia"],
        [],
        [
            Byt.__name__,
            encyklopedia["GrupaBractw"],
            miejsca["Kraj"],
            miejsca["Miejsce"],
            miejsca["Uczelnia"],
        ],
    ),
    (
        Czlonek,
        ["rok_chrztu", "miesiac_chrztu", "dzien_chrztu", "status", "staz"],
        [],
        [
            Czlonek.__name__,
            czapki["Czapka"],
            kalendarz["Chrzest"],
        ],
    ),
    (
        DawnyZarzad,
        [],
        [],
        [
            Czlonek.__name__,
            WielkiMistrz.__name__,
            kronika["Kadencja"],
            kronika["PodsumowanieKadencji"],
            kronika["WydarzenieHistoryczne"],
        ],
    ),
    (Egzekutor, [], [], [Osoba.__name__, Zespol.__name__]),
    (HallOfFame, [], [], [Osoba.__name__]),
    (ImieSzlacheckie, [], [], [Czlonek.__name__]),
    (InnaOsoba, ["kategoria"], [], [Bractwo.__name__]),
    (KomisjaRewizyjna, [], [], [Osoba.__name__, kronika["Kadencja"]]),
    (KoordynatorZespolu, [], [], [Osoba.__name__, Zespol.__name__]),
    (
        NowyZarzad,
        [],
        [],
        [
            Czlonek.__name__,
            WielkiMistrz.__name__,
            kronika["Kadencja"],
            kronika["PodsumowanieKadencji"],
            kronika["WydarzenieHistoryczne"],
        ],
    ),
    (
        Organizacja,
        ["rok_zalozenia"],
        [],
        [
            Byt.__name__,
            miejsca["Kraj"],
            miejsca["Miejsce"],
        ],
    ),
    (
        OrganizacjaStudencka,
        ["rok_zalozenia"],
        [],
        [
            Byt.__name__,
            miejsca["Kraj"],
            miejsca["Miejsce"],
            miejsca["Uczelnia"],
        ],
    ),
    (Osoba, [], [], []),
    (WielkiMistrz, [], [], [Czlonek.__name__]),
    (Zespol, [], [], [Osoba.__name__, zrodla["Dokument"]]),
    (ZwierzeCzapkowe, [], [], [Czlonek.__name__]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
