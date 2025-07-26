from .models import Dokument, Edykt, Ukaz, Zrodlo, ZrodloOgolne
from core.utils.autocompletion.AutocompletesGeneration import *

from osoby.models_dict import names as osoby

autocomplete_configs = [
    (Dokument, [], [], [osoby["Osoba"]]),
    (Edykt, [], [], [osoby["Osoba"]]),
    (Ukaz, [], [], [osoby["Osoba"]]),
    (Zrodlo, [], [], [osoby["Osoba"]]),
    (ZrodloOgolne, [], [], [osoby["Osoba"]]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
