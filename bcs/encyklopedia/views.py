from .models import *
from core.utils.automation.ViewsGeneration import *

autocomplete_configs = [
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
