from collections import defaultdict
from core.autocompletion.registry import add_model_name
from .model_imports import *

names = defaultdict(str)

add_model_name(Kadencja, names, "Kadencja")
add_model_name(PodsumowanieKadencji, names, "PodsumowanieKadencji")

add_model_name(TypWydarzeniaHistorycznego, names, "TypWydarzenieHistorycznego")
add_model_name(WydarzenieHistoryczne, names, "WydarzenieHistoryczne")

add_model_name(
    KategoriaZadaniaChrzcielnego, names, "KategoriaZadaniaChrzcielnego"
)
add_model_name(ZadanieChrzcielne, names, "ZadanieChrzcielne")
