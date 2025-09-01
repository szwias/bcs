from core.utils.autocompletion.AutocompletesGeneration import *
from .model_imports import *

autocomplete_configs = [(Zwrot, [], [], [])]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
