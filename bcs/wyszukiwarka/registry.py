from django.apps import apps

SEARCH_REGISTRY = []


def register_search(apps_to_register):
    """
    Automatically register all models in the given apps.
    - apps_to_register: list of app names (strings)
    """
    for app_label in apps_to_register:
        app_config = apps.get_app_config(app_label)
        for model in app_config.get_models():
            if getattr(model, "snippet", None):
                SEARCH_REGISTRY.append(model)
