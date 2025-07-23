from django.db.models import CharField
from django.db.models.functions import Cast

from .models import (
    CharakterystykaDzialanZarzadu,
    Kadencja,
    TypWydarzeniaHistorycznego,
    WydarzenieHistoryczne,
)
from core.utils.autocompletion.AutocompletesGeneration import *


class CustomKadencjaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Kadencja.objects.all()

        if self.q:
            qs = qs.annotate(
                rozpoczecie_str=Cast("rozpoczecie", output_field=CharField())
            ).filter(rozpoczecie_str__icontains=self.q)
        return qs


from osoby.models_dict import names as osoby

autocomplete_configs = [
    (
        CharakterystykaDzialanZarzadu,
        [],
        [],
        [osoby["Czlonek"], osoby["DawnyZarzad"], osoby["Zarzad"]],
    ),
    (Kadencja, [], ["rozpoczecie"], []),
    (TypWydarzeniaHistorycznego, [], [], []),
    (WydarzenieHistoryczne, [], [], [TypWydarzeniaHistorycznego.__name__]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(
    autocomplete_configs, globals()
)
