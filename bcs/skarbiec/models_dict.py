from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name
from .model_imports import *

names = defaultdict(str)

add_model_name(Konto, names, "Konto")
add_model_name(Transakcja, names, "Transakcja")
