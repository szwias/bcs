from collections import defaultdict
from core.utils.automation.AutocompletesGeneration import add_model_name
from .models import (
    Czapka, RodzajCzapki, \
)

names = defaultdict(str)

add_model_name(Czapka, names, "Czapka")
add_model_name(RodzajCzapki, names, "RodzajCzapki")
