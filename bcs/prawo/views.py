from .models import Podmiot, RelacjaPrawna, Struktura, Rola
from core.utils.autocompletion.AutocompletesGeneration import *

autocomplete_configs = [
    (Podmiot, [], [], []),
    (RelacjaPrawna, [], ["prawo_czy_obowiazek"], [Podmiot.__name__]),
    (Struktura, [], [], []),
    (Rola, [], [], []),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
