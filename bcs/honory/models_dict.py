from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name

from .models import (
    Nagrodzeni,
    Odznaczenie,
)

names = defaultdict(str)

add_model_name(Nagrodzeni, names, "Nagrodzeni")
add_model_name(Odznaczenie, names, "Odznaczenie")
