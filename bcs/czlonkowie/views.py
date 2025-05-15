from .models import Bean, Czlonek, DawnyZarzad, HallOfFame, ImieSzlacheckie, InnaOsoba, WielkiMistrz, \
    Zarzad, ZwierzeCzapkowe, Osoby
from core.utils.automation.ViewsGeneration import *

autocomplete_configs = [
    (Bean,              ['staz'],                                                           [], ['Czapka', 'Czlonek']),
    (Czlonek,           ['rok_chrztu', 'miesiac_chrztu', 'dzien_chrztu', 'status', 'staz'], [], ['Czapka', 'Czlonek']),
    (DawnyZarzad,       [],                                                                 [], ['Czlonek', 'core.Kadencja']),
    (HallOfFame,        [],                                                                 [], ['Czlonek']),
    (ImieSzlacheckie,   [],                                                                 [], ['Czlonek']),
    (InnaOsoba,         ['kategoria'],                                                      [], ['encyklopedia.Bractwo']),
    (Osoby,             [],                                                                 [], ['Bean', 'Czlonek', 'InnaOsoba']),
    (WielkiMistrz,      [],                                                                 [], ['Czlonek']),
    (Zarzad,            [],                                                                 [], ['Czlonek', 'core.Kadencja']),
    (ZwierzeCzapkowe,   [],                                                                 [], ['Czlonek']),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
