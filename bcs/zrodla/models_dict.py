from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name
from .models import Dokument, Edykt, Ukaz, Zrodlo, ZrodloOgolne

names = defaultdict(str)

add_model_name(Dokument, names, "Dokument")
add_model_name(Edykt, names, "Edykt")
add_model_name(Ukaz, names, "Ukaz")

add_model_name(Zrodlo, names, "Zrodlo")
add_model_name(ZrodloOgolne, names, "ZrodloOgolne")
