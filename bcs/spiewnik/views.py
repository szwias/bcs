from spiewnik.models import KategoriaPiosenki, Piosenka
from core.utils.autocompletion.AutocompletesGeneration import *

from osoby.models_dict import names as osoby

autocomplete_configs = [
    (KategoriaPiosenki, [], [], []),
    (Piosenka, [], [], [KategoriaPiosenki.__name__, osoby["Osoba"]])
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
