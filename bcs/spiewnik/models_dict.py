from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name

from .model_imports import *

names = defaultdict(str)

add_model_name(KategoriaPiosenki, names, "KategoriaPiosenki")
add_model_name(Piosenka, names, "Piosenka")
