from collections import defaultdict
from core.utils.automation.ViewsGeneration import add_model_name
from .models import (
    Kadencja, \
    )

names = defaultdict(str)

add_model_name(Kadencja, names, "Kadencja")
