# miejsca/views.py
from django.shortcuts import render
from django.http import JsonResponse

from bcs import settings
from .models import Miejsce


def mapa(request):
    # TODO: close info windows by clicking anywhere outside a window
    # TODO: add a sidebar with filters
    # Just renders the HTML template with the map
    return render(
        request=request,
        template_name="miejsca/mapa.html",
        context={"google_maps_api_key": settings.GOOGLE_MAPS_API_KEY},
    )


def mapa_dane(request):
    miejsca_qs = Miejsce.objects.filter(
        latitude__isnull=False, longitude__isnull=False
    ).select_related(
        "typ"
    )  # avoids extra queries

    miejsca_list = []
    for m in miejsca_qs:
        if "Kraj" in str(m.typ):
            continue
        miejsca_list.append(
            {
                "id": m.id,
                "nazwa": m.nazwa,
                "adres": m.adres,
                "typ": str(m.typ) if m.typ else None,
                "emoji": m.typ.emoji if m.typ else "📍",
                "closed": m.zamkniete_na_stale,
                "latitude": m.latitude,
                "longitude": m.longitude,
            }
        )

    return JsonResponse(data=miejsca_list, safe=False)
