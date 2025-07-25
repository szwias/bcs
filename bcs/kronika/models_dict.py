from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name
from .models import (
    CharakterystykaDzialanZarzadu,
    TypWydarzeniaHistorycznego,
    WydarzenieHistoryczne,
    Kadencja,
)

names = defaultdict(str)

add_model_name(
    CharakterystykaDzialanZarzadu, names, "CharakterystykaDzialanZarzadu"
)
add_model_name(Kadencja, names, "Kadencja")

add_model_name(TypWydarzeniaHistorycznego, names, "TypWydarzenieHistorycznego")
add_model_name(WydarzenieHistoryczne, names, "WydarzenieHistoryczne")
