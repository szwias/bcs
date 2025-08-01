from collections import defaultdict
from core.utils.autocompletion.AutocompletesGeneration import add_model_name
from .models import (
    Bean,
    Byt,
    Czlonek,
    DawnyZarzad,
    HallOfFame,
    ImieSzlacheckie,
    InnaOsoba,
    NowyZarzad,
    Osoba,
    WielkiMistrz,
    Zarzad,
    ZwierzeCzapkowe,
)

names = defaultdict(str)

add_model_name(Byt, names, "Byt")
add_model_name(Osoba, names, "Osoba")
add_model_name(Zarzad, names, "Zarzad")

add_model_name(Bean, names, "Bean")
add_model_name(Czlonek, names, "Czlonek")
add_model_name(InnaOsoba, names, "InnaOsoba")

add_model_name(DawnyZarzad, names, "DawnyZarzad")
add_model_name(NowyZarzad, names, "NowyZarzad")

add_model_name(ImieSzlacheckie, names, "ImieSzlacheckie")
add_model_name(WielkiMistrz, names, "WielkiMistrz")
add_model_name(ZwierzeCzapkowe, names, "ZwierzeCzapkowe")

add_model_name(HallOfFame, names, "HallOfFame")
