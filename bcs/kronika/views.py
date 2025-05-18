from .models import *
from core.utils.automation.ViewsGeneration import *

class CustomMiejsceFromWydarzenieToZdarzenieAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Miejsce.objects.all()

        wydarzenie_id = self.forwarded.get('wydarzenie', None)

        if wydarzenie_id:
            try:
                wydarzenie = Wydarzenie.objects.get(pk=wydarzenie_id)
                qs = wydarzenie.miejsca.all()
            except Wydarzenie.DoesNotExist:
                qs = Miejsce.objects.none()

        if self.q:
            qs = qs.filter(nazwa__icontains=self.q)

        return qs




autocomplete_configs = [
    (Miejsce,           ['typ'],                                [],     []),
    (Zdarzenie,         [],                                     [],     ['czlonkowie.Osoby', 'ObrazZdarzenie', 'Wydarzenie']),
    (ObrazZdarzenie,    [],                                     [],     ['Zdarzenie', 'Miejsce', 'czlonkowie.Osoby']),
    (Wydarzenie,        ['typ_wydarzenia', 'typ_wyjazdu', 'czy_to_wyjazd'],      [],     ['Miejsce', 'Zdarzenie', 'czlonkowie.Osoby']),
    (ObrazWydarzenie,   [],                                     [],     ['Wydarzenie', 'czlonkowie.Osoby']),
    (Proces,            [],                                     [],     ['Zdarzenie']),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
