from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name
from .models import (
    Chrzest,
    DepositioBeanorum,
    TypWydarzenia,
    TypWyjazdu,
    Wydarzenie,
    WydarzenieKalendarzowe,
    Zdarzenie,
)

names = defaultdict(str)

add_model_name(Chrzest, names, "Chrzest")
add_model_name(DepositioBeanorum, names, "DepositioBeanorum")
add_model_name(Wydarzenie, names, "Wydarzenie")
add_model_name(WydarzenieKalendarzowe, names, "WydarzenieKalendarzowe")
add_model_name(Zdarzenie, names, "Zdarzenie")

add_model_name(TypWydarzenia, names, "TypWydarzenia")
add_model_name(TypWyjazdu, names, "TypWyjazdu")
