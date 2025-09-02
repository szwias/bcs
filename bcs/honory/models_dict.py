from collections import defaultdict
from core.autocompletion.registry import add_model_name

from .model_imports import *

names = defaultdict(str)

add_model_name(Nagrodzeni, names, "Nagrodzeni")
add_model_name(Odznaczenie, names, "Odznaczenie")
