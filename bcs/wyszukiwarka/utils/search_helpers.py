# wyszukiwarka/utils/search_helpers.py
from collections import defaultdict

from django.apps import apps
from django.contrib.contenttypes.models import ContentType

from core.admin import get_admin_form_url
from .Search import (
    find_searchable_fields,
    adjust_snippet_classes,
    add_ellipses,
)


def search_models(query_text, models):
    """
    Search given models for query_text and return results dict suitable for templates.
    """
    results_by_app = defaultdict(lambda: defaultdict(list))
    seen = set()

    if not query_text:
        return results_by_app

    for model in models:
        searchable_fields_names = [
            f.name for f in find_searchable_fields(model)
        ]
        qs = model.objects.search(query_text=query_text, config=model.LANGUAGE)
        if not qs.exists():
            qs = model.objects.search(query_text=query_text, config="simple")

        for obj in qs:
            key = (obj._meta.label, obj.pk)
            if key in seen:
                continue
            seen.add(key)

            # Build snippet from all indexed fields
            snippets = []
            indexed_fields = set(obj.search_dict.keys()) & set(
                searchable_fields_names
            )
            for field_name in indexed_fields:
                field_snippet = getattr(obj, f"{field_name}_snippet")
                adjusted_snippet = adjust_snippet_classes(
                    add_ellipses(field_snippet, obj.search_dict[field_name]),
                    query_text,
                )
                snippets.append(
                    f"<span class='search__field'>{field_name}:</span> {adjusted_snippet}"
                )
            snippet = " ".join(snippets)

            app_label = ContentType.objects.get_for_model(obj).app_label
            app_verbose = apps.get_app_config(app_label).verbose_name
            model_name = obj._meta.verbose_name_plural

            results_by_app[app_verbose][model_name].append(
                {
                    "title": str(obj),
                    "snippet": snippet,
                    "admin_url": get_admin_form_url(obj),
                    "rank": getattr(obj, "rank", 0),
                }
            )

            print(results_by_app)

    # Sort apps and categories alphabetically, results by rank descending
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

    return sorted_results
