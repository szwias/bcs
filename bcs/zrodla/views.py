from .models import Dokument, Edykt, Ukaz, Zrodlo, ZrodloOgolne
from core.utils.autocompletion.AutocompletesGeneration import *

from osoby.models_dict import names as osoby

autocomplete_configs = [
    (Dokument, [], [], [osoby["Byt"]]),
    (Edykt, [], [], [osoby["Byt"]]),
    (Ukaz, [], [], [osoby["Byt"]]),
    (Zrodlo, [], [], [osoby["Byt"]]),
    (ZrodloOgolne, [], [], [osoby["Byt"]]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
