from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name
from .models import (
    Aforyzm,
    Bractwo,
    Cytat,
    GrupaBractw,
    Pojecie,
    TradycjaBCS,
    TradycjaInnegoBractwa,
    Zwyczaj,
)

names = defaultdict(str)

add_model_name(Bractwo, names, "Bractwo")
add_model_name(GrupaBractw, names, "GrupaBractw")

add_model_name(TradycjaBCS, names, "TradycjaBCS")
add_model_name(TradycjaInnegoBractwa, names, "TradycjaInnegoBractwa")
add_model_name(Zwyczaj, names, "Zwyczaj")

add_model_name(Pojecie, names, "Pojecie")

add_model_name(Aforyzm, names, "Aforyzm")
add_model_name(Cytat, names, "Cytat")
