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
    (
        Miejsce,
        ['typ'], [],
        []),
    (
        Zdarzenie,
        [], [],
        [ObrazZdarzenie.__name__, Wydarzenie.__name__]),
    (
        ObrazZdarzenie,
        [], [],
        [Zdarzenie.__name__, Miejsce.__name__]),
    (
        Wydarzenie,
        ['typ_wydarzenia', 'typ_wyjazdu', 'czy_to_wyjazd'], [],
        [Miejsce.__name__, Zdarzenie.__name__]),
    (
        ObrazWydarzenie,
        [], [],
        [Wydarzenie.__name__]),
    (
        Proces,
        [], [],
        [Zdarzenie.__name__]),
]

autocomplete_urls, autocomplete_widgets = setup_autocompletes(autocomplete_configs, globals())
