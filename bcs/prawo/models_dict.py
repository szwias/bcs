from collections import defaultdict
from core.autocompletion.registry import add_model_name
from .models_imports import *

names = defaultdict(str)

add_model_name(Podmiot, names, "Podmiot")
add_model_name(Rola, names, "Rola")
add_model_name(Struktura, names, "Struktura")

add_model_name(RelacjaPrawna, names, "RelacjaPrawna")

add_model_name(PrawoObowiazek, names, "PrawoObowiazek")

add_model_name(DlugoscKadencji, names, "DlugoscKadencji")
add_model_name(WielkoscStruktury, names, "WielkoscStruktury")
