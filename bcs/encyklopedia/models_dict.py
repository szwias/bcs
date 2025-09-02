from collections import defaultdict
from core.autocompletion.registry import add_model_name
from .model_imports import *

names = defaultdict(str)

add_model_name(GrupaBractw, names, "GrupaBractw")

add_model_name(TradycjaBCS, names, "TradycjaBCS")
add_model_name(TradycjaInnegoBractwa, names, "TradycjaInnegoBractwa")
add_model_name(Zwyczaj, names, "Zwyczaj")

add_model_name(Pojecie, names, "Pojecie")

add_model_name(Aforyzm, names, "Aforyzm")
add_model_name(Cytat, names, "Cytat")
add_model_name(Powiedzenie, names, "Powiedzenie")
