from dal import autocomplete

from core.autocompletion.registry import register_autocomplete
from kalendarz.models import WydarzenieKalendarzowe
from miejsca.models import Miejsce

autocomplete_urls, autocomplete_widgets = register_autocomplete(overrides={})


class CustomMiejsceFromWydarzenieKalendarzoweToZdarzenieAutocomplete(
    autocomplete.Select2QuerySetView
):
    def get_queryset(self):
        qs = Miejsce.objects.all()

        wydarzenie_id = self.forwarded.get("wydarzenie", None)

        if wydarzenie_id:
            try:
                wydarzenie = WydarzenieKalendarzowe.objects.get(
                    pk=wydarzenie_id
                )
                qs = wydarzenie.miejsca.all()
            except WydarzenieKalendarzowe.DoesNotExist:
                qs = Miejsce.objects.none()

        if self.q:
            qs = qs.filter(nazwa__icontains=self.q)

        return qs
