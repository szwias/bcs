from core.utils.autocomplete import *
from .models import Czapka, Czlonek
from django.db import models

class RokChrztuAutocomplete(FieldChoicesAutocompleteByLabel):
    model = Czlonek
    field_name = 'rok_chrztu'

class MiesiacChrztuAutocomplete(FieldChoicesAutocompleteByLabel):
    model = Czlonek
    field_name = 'miesiac_chrztu'

class DzienChrztuAutocomplete(FieldChoicesAutocompleteByLabel):
    model = Czlonek
    field_name = 'dzien_chrztu'

class StatusAutocomplete(FieldChoicesAutocompleteByLabel):
    model = Czlonek
    field_name = 'status'

class StazAutocomplete(FieldChoicesAutocompleteByLabel):
    model = Czlonek
    field_name = 'staz'

class CzapkaAutocomplete(StrMatchingAutocomplete):
    model = Czapka

class CzlonekAutocomplete(StrMatchingAutocomplete):
    model = Czlonek