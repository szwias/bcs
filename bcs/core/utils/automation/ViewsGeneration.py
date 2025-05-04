from core.utils.autocomplete import *
from django.apps import apps
from django.urls import path
from dal import autocomplete
from caseconverter import kebabcase


from functools import partial

def generate_autocomplete_views(model, label_list, value_list, model_list, globals_dict=None):
    if globals_dict is None:
        raise ValueError("globals_dict is required to register views (usually pass globals())")

    model_name = model.__name__
    app_label = model._meta.app_label
    url_patterns = []
    widgets = {}

    for field in label_list:
        view_name = f"{field.title().replace('_', '')}Autocomplete"
        view_class = type(
            view_name,
            (FieldChoicesAutocompleteByLabel,),
            {"model": model, "field_name": field},
        )
        globals_dict[view_name] = view_class

        url_name = f"{kebabcase(model_name)}-{kebabcase(field)}-by-label-autocomplete"
        url_patterns.append(path(f"{url_name}/", view_class.as_view(), name=url_name))

        widgets[field] = partial(autocomplete.ListSelect2, url=f"{app_label}:{url_name}")

    for field in value_list:
        view_name = f"{field.title().replace('_', '')}Autocomplete"
        view_class = type(
            view_name,
            (FieldChoicesAutocompleteByValue,),
            {"model": model, "field_name": field},
        )
        globals_dict[view_name] = view_class

        url_name = f"{kebabcase(model_name)}-{kebabcase(field)}-by-value-autocomplete"
        url_patterns.append(path(f"{url_name}/", view_class.as_view(), name=url_name))

        widgets[field] = partial(autocomplete.ListSelect2, url=f"{app_label}:{url_name}")

    for model_name_str in model_list:
        related_model = apps.get_model(app_label, model_name_str)
        view_name = f"{related_model.__name__}Autocomplete"
        view_class = type(
            view_name,
            (StrMatchingAutocomplete,),
            {"model": related_model, "__module__": __name__},
        )
        globals_dict[view_name] = view_class

        url_name = f"{kebabcase(model_name_str)}-records-autocomplete"
        url_patterns.append(path(f"{url_name}/", view_class.as_view(), name=url_name))

        for field in model._meta.fields:
            if getattr(field, 'related_model', None) == related_model:
                widgets[field.name] = partial(autocomplete.ModelSelect2, url=f"{app_label}:{url_name}")

    return url_patterns, {model_name: widgets}



def setup_autocompletes(configs, globals_dict):
    autocomplete_urls = []
    autocomplete_widgets = {}

    for config in configs:
        model, label_list, value_list, record_list = config

        urls, widgets = generate_autocomplete_views(
            model=model,
            label_list=label_list,
            value_list=value_list,
            model_list=record_list,
            globals_dict=globals_dict
        )

        autocomplete_urls += urls
        autocomplete_widgets.update(widgets)

    return autocomplete_urls, autocomplete_widgets

def build_widgets(widget_factories):
    return {field: factory() for field, factory in widget_factories.items()}

