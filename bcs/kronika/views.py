from .models import *
from core.utils.autocompletion.AutocompletesGeneration import *

from osoby.models_dict import names as osoby

autocomplete_configs = [
    (
        CharakterystykaDzialanZarzadu,
        [],
        [],
        [osoby["Czlonek"], osoby["DawnyZarzad"], osoby["Zarzad"]],
    ),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
