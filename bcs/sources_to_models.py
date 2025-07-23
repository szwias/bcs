from encyklopedia.models import *
from kalendarz.models import Zdarzenie, TypWydarzenia, TypWyjazdu, Wydarzenie
from kronika.models import (
    CharakterystykaDzialanZarzadu as PodsumowanieKadencji,
)
from miejsca.models import *
from osoby.models import *
from prawo.models import *

mapping = {
    "AS/Kalendarium": [
        {"kalendarium": [Wydarzenie, Zdarzenie, TypWydarzenia, TypWyjazdu]},
        {"kronika": [PodsumowanieKadencji]},
        {"miejsca": [Miejsce, TypMiejsca]},
        {"osoby": [DawnyZarzad, Zarzad, WielkiMistrz]},
    ],
    "AS/Foty": [
        {
            "encyklopedia": [
                Bractwo,
                TradycjaBCS,
                TradycjaInnegoBractwa,
                Pins,
                Pojecie,
                Zwyczaj,
            ]
        },
        {"kalendarium": [Wydarzenie, Zdarzenie]},
        {"multimedia": [ZdjecieCzapki]},
        {"osoby": [Czlonek]},
    ],
    "AS/Screeny": ["Nie otwieraj tego, bo Ci zwiesi kompa"],
    "AS/BCS_UJ": [
        {
            "encyklopedia": [
                TradycjaBCS,
                TradycjaInnegoBractwa,
                Pojecie,
                Zrodlo,
                Zwyczaj,
            ]
        },
        {"kronika": [PodsumowanieKadencji, Proces, Wydarzenie]},
    ],
    "AS/Ordre...": [{"encyklopedia": [Bractwo]}, {"osoby": [InnaOsoba]}],
    "AS/C.I.B.A.": [
        {"encyklopedia": [OrganizacjaFolkloruStudenckiego]},
        {"osoby": [InnaOsoba]},
    ],
    "AS/ASPL": [
        {"encyklopedia": [OrganizacjaFolkloruStudenckiego]},
        {"kronika": [Historia]},
        {"osoby": [InnaOsoba]},
        {"slowniczek-lacinski": [InnyZwrot]},
    ],
    "AS/FB/Ukazy_i_edykty": [
        {"dokumenty": [Edykt, Korespondencja, Ukaz]},
        {"kalendarium": [Wydarzenie, Zdarzenie]},
        {
            "kronika": [
                Historia,
                PodsumowanieKadencji,
                Wydarzenie,
                ZadanieChrzcielne,
            ]
        },
        {"encyklopedia": [Pojecie, Powiedzenie, Zwyczaj, Zrodlo]},
        {"osoby": [Czlonek, HallOfFame, InnaOsoba, WielkiMistrz]},
        {"prawo": [Obowiazek, Prawo, Rola, Struktura]},
        {"slowniczek-lacinski": [InnyZwrot]},
        {"spiewnik": [Piosenka]},
    ],
    "AS/FB/Inne": [
        {"dokumenty": [Korespondencja]},
        {"encyklopedia": [Pins, Pojecie]},
        {"kalendarium": [Wydarzenie, Zdarzenie]},
        {"kronika": [PodsumowanieKadencji, ZadanieChrzcielne]},
        {"spiewnik": [Kategoria, Piosenka]},
    ],
    "AS/FB/Ogólne": [
        {"encyklopedia": [Korporacja, Pojecie, Zrodlo]},
        {"multimedia": [ZdjecieArchiwum]},
    ],
    "AS/FB/Statuty": [
        {"dokumenty": [Statut]},
        {"encyklopedia": [Pojecie]},
        {"kronika": [Wydarzenie]},
        {"prawo": [Obowiazek, Prawo, Struktura]},
        {"slowniczek-lacinski": [InnyZwrot]},
    ],
}
