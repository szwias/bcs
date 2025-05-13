from .models import Bean, Czlonek, DawnyZarzad, HallOfFame, ImieSzlacheckie, InnaOsoba, Przezwisko, WielkiMistrz, Zarzad, ZwierzeCzapkowe
from core.utils.automation.ViewsGeneration import *

autocomplete_configs = [
    (Czlonek, ['rok_chrztu', 'miesiac_chrztu', 'dzien_chrztu', 'status', 'staz'], [], ['Czapka', 'Czlonek']),
    (Bean, ['staz'], [], ['Czapka', 'Czlonek']),
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
