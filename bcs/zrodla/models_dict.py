from collections import defaultdict
from core.autocompletion.registry import add_model_name
from .model_imports import *

names = defaultdict(str)

add_model_name(Dokument, names, "Dokument")
add_model_name(Edykt, names, "Edykt")
add_model_name(Korespondencja, names, "Korespondencja")
add_model_name(Oswiadczenie, names, "Oswiadczenie")
add_model_name(Uchwala, names, "Uchwala")
add_model_name(Ukaz, names, "Ukaz")

add_model_name(Rozliczenie, names, "Rozliczenie")

add_model_name(Zrodlo, names, "Zrodlo")
add_model_name(ZrodloOgolne, names, "ZrodloOgolne")
