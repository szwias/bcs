# drzewo/urls.py
from django.urls import path

from .views import *

app_name = "drzewo"

urlpatterns = [
    path(
        "full-tree-generation/",
        serve_full_tree_form_view,
        name="full-tree-generation",
    ),
    path(
        "scoped-tree-generation/",
        serve_scoped_tree_form_view,
        name="scoped-tree-generation",
    ),
    path(
        "full-tree-interactive/",
        full_tree_interactive_view,
        name="full_tree_interactive",
    ),
    path("full-tree-data/", full_tree_data_graphviz, name="full_tree_data"),
]
