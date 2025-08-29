from .models import (
    Dokument,
    Edykt,
    Korespondencja,
    Oswiadczenie,
    Rozliczenie,
    Ukaz,
    Zrodlo,
    ZrodloOgolne,
)
from core.utils.autocompletion.AutocompletesGeneration import *

from osoby.models_dict import names as osoby
from skarbiec.models_dict import names as skarbiec

autocomplete_configs = [
    (Dokument, [], [], [osoby["Byt"]]),
    (Edykt, [], [], [osoby["Byt"]]),
    (Korespondencja, [], [], [osoby["Byt"]]),
    (Oswiadczenie, [], [], [osoby["Byt"]]),
    (Rozliczenie, [], [], [osoby["Byt"], skarbiec["Transakcja"]]),
    (Ukaz, [], [], [osoby["Byt"]]),
    (Zrodlo, [], [], [osoby["Byt"]]),
    (ZrodloOgolne, [], [], [osoby["Byt"]]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
