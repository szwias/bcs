# wyszukiwarka/views.py
from collections import defaultdict

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from core.admin import get_admin_form_url
from .registry import SEARCH_REGISTRY
from .utils.Search import find_searchable_fields


def search(request, models=None):
    query_text = request.GET.get("q", "").strip()
    results_by_app = defaultdict(lambda: defaultdict(list))
    seen = set()

    if query_text:
        for model in SEARCH_REGISTRY:
            searchable_fields_names = [
                f.name for f in find_searchable_fields(model)
            ]
            qs = model.objects.search(
                query_text=query_text, config=model.LANGUAGE
            )
            if not qs.exists():
                qs = model.objects.search(
                    query_text=query_text, config="simple"
                )

            for obj in qs:
                key = (obj._meta.label, obj.pk)
                if key in seen:
                    continue
                seen.add(key)

                snippets = []
                indexed_fields = set(obj.search_dict.keys()) & set(
                    searchable_fields_names
                )
                for field_name in indexed_fields:
                    field_snippet = getattr(obj, f"{field_name}_snippet")
                    pair = f"<span class='field-name'>{field_name}:</span> {field_snippet}"
                    snippets.append(pair)
                snippet = " ".join(snippets)

                app_label = ContentType.objects.get_for_model(obj).app_label
                app_verbose = apps.get_app_config(app_label).verbose_name
                model_name = obj._meta.verbose_name_plural

                results_by_app[app_verbose][model_name].append(
                    {
                        "title": str(obj),
                        "snippet": snippet,
                        "admin_url": get_admin_form_url(obj),
                        "rank": obj.rank,
                    }
                )

    # Sort apps and categories alphabetically
    sorted_results = {
        app: {
            category: sorted(items, key=lambda x: x["rank"], reverse=True)
            for category, items in sorted(
                categories.items(), key=lambda x: x[0].lower()
            )
        }
        for app, categories in sorted(
            results_by_app.items(), key=lambda x: x[0].lower()
        )
    }

    return render(
        request,
        "wyszukiwarka/search_results.html",
        {"query": query_text, "results_by_app": sorted_results},
    )
