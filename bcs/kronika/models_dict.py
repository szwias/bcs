from collections import defaultdict
from core.utils.automation.AutocompletesGeneration import add_model_name
from .models import (
    Miejsce, \
    Proces, Wydarzenie, Zdarzenie, \
    ObrazWydarzenie, ObrazZdarzenie, \
    CharakterystykaDzialanZarzadu, \
    )

names = defaultdict(str)

add_model_name(Miejsce, names, "Miejsce")

add_model_name(Proces, names, "Proces")
add_model_name(Wydarzenie, names, "Wydarzenie")
add_model_name(Zdarzenie, names, "Zdarzenie")

add_model_name(ObrazWydarzenie, names, "ObrazWydarzenie")
add_model_name(ObrazZdarzenie, names, "ObrazZdarzenie")

add_model_name(CharakterystykaDzialanZarzadu, names, "CharakterystykaDzialanZarzadu")
