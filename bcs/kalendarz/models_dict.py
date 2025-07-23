from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name
from .models import (ObrazWydarzenie, ObrazZdarzenie, TypWydarzenia,
                     TypWyjazdu, Wydarzenie, Zdarzenie)

names = defaultdict(str)

add_model_name(Wydarzenie, names, "Wydarzenie")
add_model_name(Zdarzenie, names, "Zdarzenie")

add_model_name(TypWydarzenia, names, "TypWydarzenia")
add_model_name(TypWyjazdu, names, "TypWyjazdu")

add_model_name(ObrazWydarzenie, names, "ObrazWydarzenie")
add_model_name(ObrazZdarzenie, names, "ObrazZdarzenie")