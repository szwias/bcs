from core.utils.autocomplete import *
from django.apps import apps
from django.urls import path
from dal import autocomplete


def generate_autocomplete_views(model, label_list, value_list, model_list, globals_dict=None):
    """
    Generates autocomplete view classes and corresponding URL patterns and widgets.

    Returns:
        (urlpatterns: list, widgets: dict)
    """
    if globals_dict is None:
        raise ValueError("globals_dict is required to register views (usually pass globals())")

    model_name = model.__name__.lower()

    # FieldChoices by Label
    for field in label_list:
        view_name = f"{field.title().replace('_', '')}Autocomplete"
        view_class = type(
            view_name,
            (FieldChoicesAutocompleteByLabel,),
            {"model": model, "field_name": field},
        )
        globals_dict[view_name] = view_class

    # FieldChoices by Value
    for field in value_list:
        view_name = f"{field.title().replace('_', '')}Autocomplete"
        view_class = type(
            view_name,
            (FieldChoicesAutocompleteByValue,),
            {"model": model, "field_name": field},
        )
        globals_dict[view_name] = view_class

    # Records (model-based autocompletes)
    for model_name_str in model_list:
        related_model = apps.get_model(model._meta.app_label, model_name_str)
        related_model_lower = related_model.__name__.lower()
        view_name = f"{related_model.__name__}Autocomplete"
        view_class = type(
            view_name,
            (StrMatchingAutocomplete,),
            {
                "model": related_model,
                "__module__": __name__,  # ← ensures proper module registration
            },
        )
        globals_dict[view_name] = view_class

def setup_autocompletes(configs, globals_dict):
    for config in configs:
        model, label_list, value_list, record_list = config
        model_name = model.__name__

        generate_autocomplete_views(
            model=model,
            label_list=label_list,
            value_list=value_list,
            model_list=record_list,
            globals_dict=globals_dict
        )
