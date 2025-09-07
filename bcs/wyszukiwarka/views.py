# wyszukiwarka/views.py
from collections import defaultdict

from django.apps import apps
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


def search(request, models=None):
    query_text = request.GET.get("q", "").strip()
    results_by_app = defaultdict(lambda: defaultdict(list))
    seen = set()

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
                key = (obj._meta.label, obj.pk)
                if key in seen:
                    continue
                seen.add(key)

                content_type = ContentType.objects.get_for_model(obj)
                app_label = content_type.app_label

                # Get verbose name from AppConfig
                try:
                    app_verbose = apps.get_app_config(app_label).verbose_name
                except LookupError:
                    app_verbose = app_label  # fallback

                category_name = obj._meta.verbose_name_plural

                admin_url = reverse(
                    f"admin:{app_label}_{content_type.model}_change",
                    args=(quote(obj.pk),),
                )

                results_by_app[app_verbose][category_name].append(
                    {
                        "title": str(obj),
                        "snippet": obj.snippet(query_text),
                        "admin_url": admin_url,
                        "rank": obj.rank,
                    }
                )

    # Sort apps and categories alphabetically
    sorted_results = {
        app: {
            category: sorted(items, key=lambda x: x["rank"], reverse=True)
            for category, items in
            sorted(categories.items(), key=lambda x: x[0].lower())
        }
        for app, categories in
        sorted(results_by_app.items(), key=lambda x: x[0].lower())
    }

    return render(
        request,
        "wyszukiwarka/search_results.html",
        {"query": query_text, "results_by_app": sorted_results},
    )
