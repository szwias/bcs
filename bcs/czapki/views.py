from core.utils.autocompletion.AutocompletesGeneration import *
from .model_imports import *

from miejsca.models_dict import names as miejsca

autocomplete_configs = [
    (Czapka, [], [], [miejsca["Wydzial"]]),
    (RodzajCzapki, [], [], [miejsca["Kraj"]]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
