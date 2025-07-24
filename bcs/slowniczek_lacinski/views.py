from core.utils.autocompletion.AutocompletesGeneration import *
from .models import Zwrot

autocomplete_configs = [(Zwrot, [], [], [])]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
