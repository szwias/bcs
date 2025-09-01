SEARCH_REGISTRY = {}

def register_model(model, search_fields, title_field=None, snippet_func=None):
    """
    Register a model for wyszukiwarka.
    - search_fields: list of fields to search
    - title_field: field to use as title
    - snippet_func: function(instance) -> string for snippet
    """
    SEARCH_REGISTRY[model] = {
        "search_fields": search_fields,
        "title_field": title_field,
        "snippet_func": snippet_func,
    }

def get_registered_models():
    return SEARCH_REGISTRY.keys()
