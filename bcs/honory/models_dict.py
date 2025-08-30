from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name

from .models import (
    Odznaczenie,
)

names = defaultdict(str)

add_model_name(Odznaczenie, names, "Odznaczenie")
