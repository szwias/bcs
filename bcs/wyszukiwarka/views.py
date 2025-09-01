from django.shortcuts import render
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from kronika.models import PodsumowanieKadencji as P

def search(request):
    q = request.GET.get("q", "")
    results = []
    if q:
        query = SearchQuery(q)
        results_qs = (
            P.objects.annotate(rank=SearchRank(SearchVector("podsumowanie"), query))
            .filter(podsumowanie__search=q)
            .order_by("-rank")
        )

        for obj in results_qs:
            results.append({
                "title": str(obj),
                "snippet": obj.podsumowanie[:150],
                "admin_url": f"/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/change/"
            })

    return render(request, "wyszukiwarka/search_results.html", {"results": results, "query": q})
