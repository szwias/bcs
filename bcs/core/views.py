from core.models import Kadencja
from django.db.models import CharField
from django.db.models.functions import Cast
from core.utils.autocompletion.AutocompletesGeneration import *

class CustomKadencjaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Kadencja.objects.all()

        if self.q:
            qs = qs.annotate(
                rozpoczecie_str=Cast('rozpoczecie', output_field=CharField())
            ).filter(
                rozpoczecie_str__icontains=self.q
            )
        return qs

autocomplete_configs = [
    (
        Kadencja,
        [], ['rozpoczecie'],
        [])
]
autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())