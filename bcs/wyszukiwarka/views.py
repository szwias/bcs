# wyszukiwarka/views.py
from django.shortcuts import render

from .registry import SEARCH_REGISTRY
from .utils.search_helpers import search_models


def search(request, models=None):
    query_text = request.GET.get("q", "").strip()
    if models is None:
        models = SEARCH_REGISTRY

    results_by_app = search_models(query_text, models)

    return render(
        request,
        "wyszukiwarka/search_results.html",
        {"query": query_text, "results_by_app": results_by_app},
    )
