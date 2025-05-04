from core.utils.autocomplete import *
from django.apps import apps
from django.urls import path
from dal import autocomplete


def generate_autocomplete_views(model, label_list, value_list, model_list, globals_dict=None, url_prefix="", namespace=None):
    """
    Generates autocomplete view classes and corresponding URL patterns and widgets.

    Returns:
        (urlpatterns: list, widgets: dict)
    """
    if globals_dict is None:
        raise ValueError("globals_dict is required to register views (usually pass globals())")

    urlpatterns = []
    widgets = {}
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
        urlpatterns.append(
            path(
                f"{url_prefix}{model_name}/{field}/autocomplete/",
                view_class.as_view(),
                name=f"{model_name}_{field}_label_autocomplete"
            )
        )
        url_name = f"{model_name}_{field}_label_autocomplete"
        if namespace:
            url_name = f"{namespace}:{url_name}"
        widgets[field] = autocomplete.ListSelect2(url=url_name)

    # FieldChoices by Value
    for field in value_list:
        view_name = f"{field.title().replace('_', '')}Autocomplete"
        view_class = type(
            view_name,
            (FieldChoicesAutocompleteByValue,),
            {"model": model, "field_name": field},
        )
        globals_dict[view_name] = view_class
        urlpatterns.append(
            path(
                f"{url_prefix}{model_name}/{field}/autocomplete/",
                view_class.as_view(),
                name=f"{model_name}_{field}_value_autocomplete"
            )
        )
        url_name = f"{model_name}_{field}_value_autocomplete"
        if namespace:
            url_name = f"{namespace}:{url_name}"
        widgets[field] = autocomplete.ListSelect2(url=url_name)

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
        urlpatterns.append(
            path(
                f"{url_prefix}{related_model_lower}/autocomplete/",
                view_class.as_view(),
                name=f"{related_model_lower}_records_autocomplete"
            )
        )

    return urlpatterns, widgets


from django.utils.text import slugify


def setup_autocompletes(configs, globals_dict, namespace, url_prefix=""):
    urlpatterns = []
    widgets_per_model = {}

    for config in configs:
        model, label_list, value_list, record_list = config
        model_name = model.__name__

        model_urlpatterns, model_widgets = generate_autocomplete_views(
            model=model,
            label_list=label_list,
            value_list=value_list,
            model_list=record_list,
            globals_dict=globals_dict,
            namespace=namespace,
            url_prefix=url_prefix,
        )

        urlpatterns.extend(model_urlpatterns)
        widgets_per_model[model_name.lower()] = model_widgets

    return urlpatterns, widgets_per_model
