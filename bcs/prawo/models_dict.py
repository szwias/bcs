from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name
from .models import (Podmiot, RelacjaPrawna, Rola,
                     Struktura)

names = defaultdict(str)

add_model_name(Podmiot, names, "Podmiot")
add_model_name(Rola, names, "Rola")
add_model_name(Struktura, names, "Struktura")

add_model_name(RelacjaPrawna, names, "RelacjaPrawna")