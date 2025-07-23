from kronika.models import *
from miejsca.models import *
from osoby.models import *
from prawo.models import *

mapping = {
    "Kalendarium Czapki od Tadka i Kaspra aż do chwili obecnej": [
        {"kronika": [Wydarzenie, Zdarzenie, TypWydarzenia,
                     TypWyjazdu, CharakterystykaDzialanZarzadu]},
        {"miejsca": [Miejsce, TypMiejsca]},
        {"osoby": [DawnyZarzad, Zarzad, WielkiMistrz]},
    ],
    "Ukazy/Edykty": [
        {"osoby": [Czlonek, HallOfFame]},
        {"prawo": [Ukaz, Edykt, Prawo, Obowiazek]},
    ]
}
