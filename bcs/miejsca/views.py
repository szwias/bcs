from django.shortcuts import render
from django.http import JsonResponse

from .models import Miejsce


def miejsca_map(request):
    # Just renders the HTML template with the map
    return render(request, "miejsca/mapa.html")


def miejsca_map_data(request):
    miejsca_qs = Miejsce.objects.filter(
        latitude__isnull=False, longitude__isnull=False
    ).select_related(
        "typ"
    )  # avoids extra queries

    miejsca_list = []
    for m in miejsca_qs:
        miejsca_list.append(
            {
                "id": m.id,
                "nazwa": m.nazwa,
                "adres": m.adres,
                "typ": str(m.typ) if m.typ else None,  # <-- str(typ) here
                "closed": m.zamkniete_na_stale,
                "latitude": m.latitude,
                "longitude": m.longitude,
            }
        )

    return JsonResponse(miejsca_list, safe=False)
