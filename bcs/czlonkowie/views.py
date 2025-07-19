from .models import OldBean, OldCzlonek, Bean, Czlonek, InnaOsoba, DawnyZarzad, HallOfFame, ImieSzlacheckie, InnaOldOsoba, WielkiMistrz, \
    Zarzad, ZwierzeCzapkowe
from core.utils.automation.AutocompletesGeneration import *

from core.models_dict import names as core
from czapki.models_dict import names as czapki
from encyklopedia.models_dict import names as encyklopedia
from kronika.models_dict import names as kronika

autocomplete_configs = [
    (
        OldBean,
        ['staz'], [],
        [czapki['Czapka'], OldCzlonek.__name__]),
    (
        OldCzlonek,
        ['rok_chrztu', 'miesiac_chrztu', 'dzien_chrztu', 'status', 'staz'], [],
        [czapki['Czapka'], OldCzlonek.__name__]),
    (
        Bean,
        ['staz'], [],
        [czapki['Czapka'], Czlonek.__name__]),
    (
        Czlonek,
        ['rok_chrztu', 'miesiac_chrztu', 'dzien_chrztu', 'status', 'staz'], [],
        [czapki['Czapka'], Czlonek.__name__]),
    (
        DawnyZarzad,
        [], [],
        [WielkiMistrz.__name__, OldCzlonek.__name__, core['Kadencja'], kronika['CharakterystykaDzialanZarzadu']]),
    (
        HallOfFame,
        [], [],
        [OldCzlonek.__name__, OldBean.__name__]),
    (
        ImieSzlacheckie,
        [], [],
        [OldCzlonek.__name__]),
    (
        InnaOldOsoba,
        ['kategoria'], [],
        [encyklopedia['Bractwo']]),
    (
        InnaOsoba,
        ['kategoria'], [],
        [encyklopedia['Bractwo']]),
    (
        WielkiMistrz,
        [], [],
        [OldCzlonek.__name__]),
    (
        Zarzad,
        [], [],
        [WielkiMistrz.__name__, OldCzlonek.__name__, core['Kadencja'], kronika['CharakterystykaDzialanZarzadu']]),
    (
        ZwierzeCzapkowe,
        [], [],
        [OldCzlonek.__name__]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
