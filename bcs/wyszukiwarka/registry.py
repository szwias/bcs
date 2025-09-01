from django.apps import apps

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


def register_search(apps_to_register, snippet_attr="snippet"):
    """
    Automatically register all models in the given apps.
    - apps_to_register: list of app names (strings)
    - snippet_attr: the method to call on model instances for snippet
    """

    for app_label in apps_to_register:
        app_config = apps.get_app_config(app_label)
        for model in app_config.get_models():
            # Only register models that actually have the snippet method
            snippet_func = getattr(model, snippet_attr, None)
            if snippet_func is None:
                pass

            register_model(
                model,
                search_fields=[f.name for f in model._meta.get_fields()],
                title_field=None,  # use __str__() by default
                snippet_func=snippet_func,
            )

