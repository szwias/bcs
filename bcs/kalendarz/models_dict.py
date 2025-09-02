from collections import defaultdict
from core.autocompletion.registry import add_model_name
from .model_imports import *

names = defaultdict(str)

add_model_name(Chrzest, names, "Chrzest")
add_model_name(Wydarzenie, names, "Wydarzenie")
add_model_name(WydarzenieKalendarzowe, names, "WydarzenieKalendarzowe")
add_model_name(Zdarzenie, names, "Zdarzenie")

add_model_name(TypWydarzenia, names, "TypWydarzenia")
add_model_name(TypWyjazdu, names, "TypWyjazdu")
