from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name
from .models import (
    Czapka,
    CzapkaHonorisCausa,
    RodzajCzapki,
)

names = defaultdict(str)

add_model_name(Czapka, names, "Czapka")
add_model_name(CzapkaHonorisCausa, names, "CzapkaHonorisCausa")
add_model_name(RodzajCzapki, names, "RodzajCzapki")
