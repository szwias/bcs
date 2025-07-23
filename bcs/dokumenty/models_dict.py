from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name
from dokumenty.models import Dokument, Edykt, Ukaz

names = defaultdict(str)

add_model_name(Dokument, names, "Dokument")
add_model_name(Edykt, names, "Edykt")
add_model_name(Ukaz, names, "Ukaz")
