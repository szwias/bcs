from core.utils.autocomplete import *
from .models import *

class TypWydarzeniaAutocomplete(FieldChoicesAutocompleteByLabel):
    model = Wydarzenie
    field_name = 'typ'

class TypMiejscaAutocomplete(FieldChoicesAutocompleteByLabel):
    model = Miejsce
    field_name = 'typ'

class TypWyjazduAutocomplete(FieldChoicesAutocompleteByLabel):
    model = Wyjazd
    field_name = 'typ'

class MiejsceAutocomplete(StrMatchingAutocomplete):
    model = Miejsce

class ZdarzenieAutocomplete(StrMatchingAutocomplete):
    model = Zdarzenie