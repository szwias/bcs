from core.utils.autocompletion.AutocompletesGeneration import *
from .models import (
    Czapka,
    CzapkaHonorisCausa,
    RodzajCzapki,
)

from miejsca.models_dict import names as miejsca
from osoby.models_dict import names as osoby
from zrodla.models_dict import names as zrodla

autocomplete_configs = [
    (Czapka, [], [], [miejsca["Wydzial"]]),
    (CzapkaHonorisCausa, [], [], [osoby["Osoba"], zrodla["Dokument"]]),
    (RodzajCzapki, [], [], [miejsca["Kraj"]]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
