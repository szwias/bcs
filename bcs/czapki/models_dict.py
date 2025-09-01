from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name
from .model_imports import *

names = defaultdict(str)

add_model_name(Czapka, names, "Czapka")
add_model_name(RodzajCzapki, names, "RodzajCzapki")
