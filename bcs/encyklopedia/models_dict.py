from collections import defaultdict
from core.utils.automation.ViewsGeneration import add_model_name
from .models import (
    Bractwo, \
    TradycjaBCS, TradycjaInnegoBractwa, \
    Powiedzenie, Zwyczaj, \
    )

names = defaultdict(str)

add_model_name(Bractwo, names, "Bractwo")

add_model_name(TradycjaBCS, names, "TradycjaBCS")
add_model_name(TradycjaInnegoBractwa, names, "TradycjaInnegoBractwa")

add_model_name(Powiedzenie, names, "Powiedzenie")
add_model_name(Zwyczaj, names, "Zwyczaj")
