from models import *
from core.utils.autocompletion.AutocompletesGeneration import *

from core.models_dict import names as core
from encyklopedia.models_dict import names as encyklopedia
from kronika.models_dict import names as kronika

autocomplete_configs = []

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
