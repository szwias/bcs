# wyszukiwarka/views.py
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
    results = []
    seen = set()  # track already added objects (model + pk)

    if query_text:
        search_query = SearchQuery(query_text)

        for model in SEARCH_REGISTRY:
            qs = (
                model.objects.annotate(
                    rank=SearchRank(search_vector,search_query)
                ).filter(rank__gt=0).order_by("-rank").distinct()
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

                results.append(
                    {
                        "title": obj.title,
                        "snippet": obj.snippet(query_text),
                        "admin_url": admin_url,
                    }
                )

    return render(
        request,
        "wyszukiwarka/search_results.html",
        {"query": query_text, "results": results},
    )
