# wyszukiwarka/views.py
from collections import defaultdict

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.contrib.admin.utils import quote
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
)
from django.shortcuts import render
from .registry import SEARCH_REGISTRY


def search(request):
    query_text = request.GET.get("q", "").strip()
    results_by_type = defaultdict(list)
    seen = set()  # track already added objects (model + pk)

    if query_text:
        search_query = SearchQuery(query_text, config="polish")
        search_vector = SearchVector("search_text", config="polish")

        for model in SEARCH_REGISTRY:
            qs = (
                model.objects.annotate(
                    rank=SearchRank(search_vector, search_query)
                )
                .filter(rank__gt=0)
                .order_by("-rank")
                .distinct()
            )

            for obj in qs:
                key = (obj._meta.label, obj.pk)  # Globally unique key
                if key in seen:
                    continue
                seen.add(key)

                # admin URL
                content_type = ContentType.objects.get_for_model(obj)
                admin_url = reverse(
                    f"admin:{content_type.app_label}_{content_type.model}_change",
                    args=(quote(obj.pk),),
                )

                # Use verbose_name_plural as grouping key
                group_name = getattr(
                    obj._meta, "verbose_name_plural", obj._meta.model_name
                )

                results_by_type[group_name].append(
                    {
                        "title": str(obj),
                        "snippet": obj.snippet(query_text),
                        "admin_url": admin_url,
                    }
                )

    # Sort categories alphabetically
    sorted_results = dict(
        sorted(results_by_type.items(), key=lambda x: x[0].lower())
    )

    return render(
        request,
        "wyszukiwarka/search_results.html",
        {"query": query_text, "results_by_type": sorted_results},
    )
