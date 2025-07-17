from core.utils.automation.AutocompletesGeneration import *
from .models import Czapka

from miejsca.models_dict import names as miejsca

autocomplete_configs = [
    (
        Czapka,
        [], [],
        [miejsca['Wydzial']]
    ),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
