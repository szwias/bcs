from .models import (
    # OldBean, Czlonek, \
    Bean, Czlonek, InnaOsoba, DawnyZarzad, HallOfFame, ImieSzlacheckie, \
    # InnaOldOsoba, \
    WielkiMistrz, \
    Zarzad, ZwierzeCzapkowe, \
)
from core.utils.automation.AutocompletesGeneration import *

from core.models_dict import names as core
from czapki.models_dict import names as czapki
from encyklopedia.models_dict import names as encyklopedia
from kronika.models_dict import names as kronika

autocomplete_configs = [
    # (
    #     OldBean,
    #     ['staz'], [],
    #     [czapki['Czapka'], Czlonek.__name__]),
    # (
    #     Czlonek,
    #     ['rok_chrztu', 'miesiac_chrztu', 'dzien_chrztu', 'status', 'staz'], [],
    #     [czapki['Czapka'], Czlonek.__name__]),
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
        [WielkiMistrz.__name__, Czlonek.__name__, core['Kadencja'], kronika['CharakterystykaDzialanZarzadu']]),
    (
        HallOfFame,
        [], [],
        [Czlonek.__name__, Bean.__name__]),
    (
        ImieSzlacheckie,
        [], [],
        [Czlonek.__name__]),
    # (
    #     InnaOldOsoba,
    #     ['kategoria'], [],
    #     [encyklopedia['Bractwo']]),
    (
        InnaOsoba,
        ['kategoria'], [],
        [encyklopedia['Bractwo']]),
    (
        WielkiMistrz,
        [], [],
        [Czlonek.__name__]),
    (
        Zarzad,
        [], [],
        [WielkiMistrz.__name__, Czlonek.__name__, core['Kadencja'], kronika['CharakterystykaDzialanZarzadu']]),
    (
        ZwierzeCzapkowe,
        [], [],
        [Czlonek.__name__]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
