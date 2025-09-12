import inspect

from django.apps import AppConfig, apps


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Jądro projektu"


def get_calling_app_config():
    """
    Returns the AppConfig of the app from which this function was called.
    """
    caller_frame = inspect.stack()[
        2
    ]  # two levels up to skip this function and register function
    module = inspect.getmodule(caller_frame[0])
    if not module:
        return None
    module_name = module.__name__  # e.g., "myapp.views"
    app_label = module_name.split(".")[0]
    try:
        return apps.get_app_config(app_label)
    except LookupError:
        return None
