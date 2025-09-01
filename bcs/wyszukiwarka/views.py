from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from kronika.models import PodsumowanieKadencji

def search(request):
    q = request.GET.get("q", "")
    results = []

    if query:
        search_vector = SearchVector("podsumowanie")
        search_query = SearchQuery(query)

        results = (
            # PodsumowanieKadencji.objects
            # .annotate(rank=SearchRank(search_vector, search_query))
            # .filter(rank__gte=0.1)  # optional: filter out very low matches
            # .order_by("-rank")
            PodsumowanieKadencji.objects.annotate(
                vector=search_vector
            ).filter(vector=search_query)
        )

    return render(request, "wyszukiwarka/search_results.html", {
        "query": query,
        "results": results,
    })
