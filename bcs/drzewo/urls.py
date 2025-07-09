# drzewo/urls.py
from django.urls import path
from .views import serve_full_tree_form_view, serve_scoped_tree_form_view

app_name = 'drzewo'

urlpatterns = [
    path("full-tree-generation/", serve_full_tree_form_view, name="full-tree-generation"),
    path("scoped-tree-generation/", serve_scoped_tree_form_view, name="scoped-tree-generation"),
]
