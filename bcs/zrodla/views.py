from .model_imports import *
from core.utils.autocompletion.AutocompletesGeneration import *

from kronika.models_dict import names as kronika
from osoby.models_dict import names as osoby
from skarbiec.models_dict import names as skarbiec

autocomplete_configs = [
    (Dokument, [], [], [osoby["Byt"]]),
    (Edykt, [], [], [osoby["Byt"]]),
    (Korespondencja, [], [], [osoby["Byt"]]),
    (Oswiadczenie, [], [], [osoby["Byt"]]),
    (Rozliczenie, [], [], [osoby["Byt"], skarbiec["Transakcja"]]),
    (Uchwala, [], [], [kronika["WydarzenieHistoryczne"], osoby["Byt"]]),
    (Ukaz, [], [], [osoby["Byt"]]),
    (Zrodlo, [], [], [osoby["Byt"]]),
    (ZrodloOgolne, [], [], [osoby["Byt"]]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
