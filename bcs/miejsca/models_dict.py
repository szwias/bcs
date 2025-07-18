from collections import defaultdict
from core.utils.automation.AutocompletesGeneration import add_model_name
from .models import (
    Kraj, Miejsce, \
    Uczelnia, Wydzial, \
)

names = defaultdict(str)

add_model_name(Kraj, names, 'Kraj')
add_model_name(Miejsce, names, 'Miejsce')

add_model_name(Uczelnia, names, 'Uczelnia')
add_model_name(Wydzial, names, 'Wydzial')