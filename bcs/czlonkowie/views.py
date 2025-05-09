from .models import Czlonek, ImieSzlacheckie, ZwierzeCzapkowe, WielkiMistrz, HallOfFame, DawnyZarzad, Zarzad, Kadencja, \
    InnaOsoba, Przezwisko
from core.utils.automation.ViewsGeneration import *

autocomplete_configs = [
    (Czlonek, ['rok_chrztu', 'miesiac_chrztu', 'dzien_chrztu', 'status', 'staz'], [], ['Czapka', 'Czlonek']),
    (ImieSzlacheckie, [], [], ['Czlonek']),
    (ZwierzeCzapkowe, [], [], ['Czlonek']),
    (WielkiMistrz, [], [], ['Czlonek']),
    (HallOfFame, [], [], ['Czlonek']),
    (DawnyZarzad, [], [], ['Czlonek', 'core.Kadencja']),
    (Zarzad, [], [], ['Czlonek', 'core.Kadencja']),
    (InnaOsoba, ['kategoria'], [], []),
    (Przezwisko, [], [], ['Czlonek'])
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
