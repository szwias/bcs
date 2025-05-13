from datetime import datetime

ROK_ZALOZENIA = 2009
BIEZACY_ROK = datetime.now().year
LATA = [(i, str(i)) for i in range(ROK_ZALOZENIA, BIEZACY_ROK + 1)]
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
    "grudzień"]
MIESIACE = list(zip(range(1, 13), nazwy_miesiecy))
DNI = [(i, str(i)) for i in range(1, 32)]
