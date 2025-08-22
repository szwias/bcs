from .models import *
from core.utils.autocompletion.AutocompletesGeneration import *

from czapki.models_dict import names as czapki
from kalendarz.models_dict import names as kalendarz
from miejsca.models_dict import names as miejsca
from osoby.models_dict import names as osoby
from zrodla.models_dict import names as zrodla

autocomplete_configs = [
    (Aforyzm, [], [], [osoby["Byt"], osoby["Osoba"], zrodla["Zrodlo"]]),
    (
        Bractwo,
        ["wiek_tradycje", "rok_zalozenia"],
        [],
        [GrupaBractw.__name__, miejsca["Kraj"], osoby["Osoba"]],
    ),
    (Cytat, [], [], [osoby["Byt"], osoby["Osoba"], zrodla["Zrodlo"]]),
    (GrupaBractw, [], [], [czapki["RodzajCzapki"], miejsca["Kraj"]]),
    (
        Pojecie,
        ["origins"],
        [],
        [kalendarz["WydarzenieKalendarzowe"], osoby["Byt"], zrodla["Zrodlo"]],
    ),
    (Powiedzenie, [], [], [osoby["Byt"], osoby["Osoba"], zrodla["Zrodlo"]]),
    (
        TradycjaBCS,
        [
            "okolicznosci_powstania",
            "zapozyczona_czy_autorska",
            "pewnosc_stazu",
        ],
        [],
        [GrupaBractw.__name__, kalendarz["WydarzenieKalendarzowe"], osoby["Osoba"]],
    ),
    (TradycjaInnegoBractwa, [], [], [GrupaBractw.__name__]),
    (Zwyczaj, [], [], [osoby["Osoba"]]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
