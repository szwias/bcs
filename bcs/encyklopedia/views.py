from .models import *
from core.utils.autocompletion.AutocompletesGeneration import *

from czapki.models_dict import names as czapki
from osoby.models_dict import names as osoby
from kalendarz.models_dict import names as kalendarz
from miejsca.models_dict import names as miejsca

autocomplete_configs = [
    (
        Bractwo,
        ["wiek_tradycje", "rok_zalozenia"],
        [],
        [
            GrupaBractw.__name__,
            miejsca["Kraj"],
            osoby["Osoba"],
        ],
    ),
    (GrupaBractw, [], [], [czapki["RodzajCzapki"], miejsca["Kraj"]]),
    (Pojecie, ["origins"], [], [kalendarz["Wydarzenie"], osoby["Osoba"]]),
    (Powiedzenie, [], [], [osoby["Osoba"]]),
    (
        TradycjaBCS,
        ["okolicznosci_powstania", "zapozyczona_czy_autorska"],
        [],
        [
            GrupaBractw.__name__,
            kalendarz["Wydarzenie"],
            osoby["Osoba"],
        ],
    ),
    (TradycjaInnegoBractwa, [], [], [GrupaBractw.__name__]),
    (Zwyczaj, [], [], [osoby["Osoba"]]),
    (Zrodlo, [], [], [osoby["Osoba"]]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
