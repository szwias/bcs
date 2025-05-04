from .utils.autocomplete import *
from .utils.czas.models import Kadencja
from django.db.models import CharField
from django.db.models.functions import Cast

# Create your views here.
class RozpoczecieAutocomplete(FieldChoicesAutocompleteByValue):
    model = Kadencja
    field_name = 'rozpoczecie'

class KadencjaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Kadencja.objects.all()

        if self.q:
            qs = qs.annotate(
                rozpoczecie_str=Cast('rozpoczecie', output_field=CharField())
            ).filter(
                rozpoczecie_str__icontains=self.q
            )
        return qs