from .models import Bean, Czlonek, DawnyZarzad, HallOfFame, ImieSzlacheckie, InnaOsoba, WielkiMistrz, \
    Zarzad, ZwierzeCzapkowe, Osoby
from core.utils.automation.ViewsGeneration import *

autocomplete_configs = [
    (Bean,              ['staz'],                                                           [], ['Czapka', 'Czlonek']),
    (Czlonek,           ['rok_chrztu', 'miesiac_chrztu', 'dzien_chrztu', 'status', 'staz'], [], ['Czapka', 'Czlonek']),
    (DawnyZarzad,       [],                                                                 [], ['WielkiMistrz', 'Czlonek', 'core.Kadencja', 'kronika.CharakterystykaDzialanZarzadu']),
    (HallOfFame,        [],                                                                 [], ['Czlonek', 'Bean']),
    (ImieSzlacheckie,   [],                                                                 [], ['Czlonek']),
    (InnaOsoba,         ['kategoria'],                                                      [], ['encyklopedia.Bractwo']),
    (Osoby,             [],                                                                 [], ['Bean', 'Czlonek', 'InnaOsoba']),
    (WielkiMistrz,      [],                                                                 [], ['Czlonek']),
    (Zarzad,            [],                                                                 [], ['WielkiMistrz', 'Czlonek', 'core.Kadencja', 'kronika.CharakterystykaDzialanZarzadu']),
    (ZwierzeCzapkowe,   [],                                                                 [], ['Czlonek']),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
