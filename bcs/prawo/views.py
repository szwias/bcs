from .models import *
from core.utils.autocompletion.AutocompletesGeneration import *


autocomplete_configs = [

]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
