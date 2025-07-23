from datetime import datetime
from roman import toRoman

ZALOZENIE_PIERWSZEGO_UNIWERSYTETU = 1000
ROK_ZALOZENIA = 2009
BIEZACY_ROK = datetime.now().year
LATA_BCS = [(i, str(i)) for i in range(ROK_ZALOZENIA, BIEZACY_ROK + 1)]
LATA_BRACTW = [
    (i, str(i)) for i in range(ZALOZENIE_PIERWSZEGO_UNIWERSYTETU, BIEZACY_ROK)
]
WIEKI = [(i, toRoman(i)) for i in range(11, BIEZACY_ROK // 100 + 1)]
MAKSYMALNA_ILOSC_POKOLEN = 3 * (BIEZACY_ROK - ROK_ZALOZENIA + 1)
nazwy_miesiecy = [
    "styczeń",
    "luty",
    "marzec",
    "kwiecień",
    "maj",
    "czerwiec",
    "lipiec",
    "sierpień",
    "wrzesień",
    "październik",
    "listopad",
    "grudzień",
]
MIESIACE = list(zip(range(1, 13), nazwy_miesiecy))
DNI = [(i, str(i)) for i in range(1, 32)]
