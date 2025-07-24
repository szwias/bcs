from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name
from .models import Zwrot

names = defaultdict(str)

add_model_name(Zwrot, names, "Zwrot")