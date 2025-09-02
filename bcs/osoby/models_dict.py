from collections import defaultdict
from core.autocompletion.registry import add_model_name
from .model_imports import *

names = defaultdict(str)

add_model_name(Byt, names, "Byt")
add_model_name(Organizacja, names, "Organizacja")
add_model_name(Osoba, names, "Osoba")
add_model_name(Zarzad, names, "Zarzad")

add_model_name(OrganizacjaStudencka, names, "OrganizacjaStudencka")
add_model_name(Bractwo, names, "Bractwo")

add_model_name(Bean, names, "Bean")
add_model_name(Czlonek, names, "Czlonek")
add_model_name(InnaOsoba, names, "InnaOsoba")

add_model_name(DawnyZarzad, names, "DawnyZarzad")
add_model_name(NowyZarzad, names, "NowyZarzad")

add_model_name(Egzekutor, names, "Egzekutor")
add_model_name(KoordynatorZespolu, names, "KoordynatorZespolu")
add_model_name(Zespol, names, "Zespol")

add_model_name(ImieSzlacheckie, names, "ImieSzlacheckie")
add_model_name(KomisjaRewizyjna, names, "KomisjaRewizyjna")
add_model_name(WielkiMistrz, names, "WielkiMistrz")
add_model_name(ZwierzeCzapkowe, names, "ZwierzeCzapkowe")

add_model_name(HallOfFame, names, "HallOfFame")
