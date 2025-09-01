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

        for model, config in SEARCH_REGISTRY.items():
            vector = SearchVector(*config["search_fields"])
            qs = (
                model.objects.annotate(rank=SearchRank(vector, search_query))
                .filter(rank__gt=0)
                .order_by("-rank")[:10]
            )

            for obj in qs:
                key = (model.__name__, obj.pk)
                if key in seen:
                    continue  # skip duplicates
                seen.add(key)

                # title and snippet
                title = (
                    getattr(obj, config["title_field"])
                    if config.get("title_field")
                    else str(obj)
                )
                snippet = (
                    config["snippet_func"](obj)
                    if config.get("snippet_func")
                    else str(obj)
                )

                # admin URL
                content_type = ContentType.objects.get_for_model(obj)
                admin_url = reverse(
                    f"admin:{content_type.app_label}_{content_type.model}_change",
                    args=(quote(obj.pk),),
                )

                results.append(
                    {
                        "title": title,
                        "snippet": snippet,
                        "admin_url": admin_url,
                    }
                )

    return render(
        request,
        "wyszukiwarka/search_results.html",
        {"query": query_text, "results": results},
    )
