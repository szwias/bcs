from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name
from .models import (
    Kadencja,
    PodsumowanieKadencji,
    TypWydarzeniaHistorycznego,
    WydarzenieHistoryczne,
    ZadanieChrzcielne,
)

names = defaultdict(str)

add_model_name(Kadencja, names, "Kadencja")
add_model_name(PodsumowanieKadencji, names, "PodsumowanieKadencji")

add_model_name(TypWydarzeniaHistorycznego, names, "TypWydarzenieHistorycznego")
add_model_name(WydarzenieHistoryczne, names, "WydarzenieHistoryczne")

add_model_name(ZadanieChrzcielne, names, "ZadanieChrzcielne")
