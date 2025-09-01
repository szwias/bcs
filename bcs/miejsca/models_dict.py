from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name
from .model_imports import *

names = defaultdict(str)

add_model_name(Kraj, names, "Kraj")
add_model_name(Miejsce, names, "Miejsce")
add_model_name(TypMiejsca, names, "TypMiejsca")

add_model_name(Uczelnia, names, "Uczelnia")
add_model_name(Wydzial, names, "Wydzial")
