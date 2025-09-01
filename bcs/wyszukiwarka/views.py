# wyszukiwarka/views.py
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.contrib.admin.utils import quote
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.shortcuts import render
from .registry import SEARCH_REGISTRY

def search(request):
    q = request.GET.get("q", "")
    results = []

    if q:
        for model, config in SEARCH_REGISTRY.items():
            vector = SearchVector(*config["search_fields"])
            query = SearchQuery(q)
            qs = (
                model.objects.annotate(rank=SearchRank(vector, query))
                .filter(rank__gt=0)
                .order_by("-rank")[:10]
            )

            for obj in qs:
                title = getattr(obj, config["title_field"]) if config["title_field"] else str(obj)
                snippet = config["snippet_func"](obj) if config["snippet_func"] else str(obj)

                # build admin URL
                content_type = ContentType.objects.get_for_model(obj)
                app_name = content_type.app_label
                model_name = content_type.model
                admin_url = reverse(f"admin:{app_name}_{model_name}_change", args=(quote(obj.pk),))

                results.append({
                    "title": title,
                    "snippet": snippet,
                    "admin_url": admin_url,
                })

    return render(request, "wyszukiwarka/search_results.html", {"query": q, "results": results})
