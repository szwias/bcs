from dal import autocomplete
from kronika.models import Wydarzenie
from miejsca.models import Miejsce

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