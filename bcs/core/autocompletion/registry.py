from caseconverter import kebabcase
from dal import autocomplete
from functools import partial

from django.urls import path
from django.db.models import CharField, IntegerField

from core.apps import get_calling_app_config
from .autocomplete import (
    FieldChoicesAutocompleteByLabel,
    FieldChoicesAutocompleteByValue,
    StrMatchingAutocomplete,
)


def register_autocomplete(overrides=None):
    """
    Dynamically registers autocomplete views and widgets for all models in the
    calling Django app.

    This function:
      - Iterates through all models of the app from which it's called.
      - Dynamically creates DRF-based autocomplete views for:
          1. **Label fields**: CharFields or IntegerFields with `choices`.
          2. **Value fields**: Arbitrary fields specified in overrides.
          3. **Related models**: All ForeignKey or OneToOne related models.
      - Builds URL patterns for these views.
      - Prepares `dal.autocomplete` widgets for use in forms and admin.

    Arguments:
        overrides (dict, optional):
            A dictionary for per-model customization of autocomplete behavior.
            Keys are model class names (str), values are dicts with keys:
                - "label_fields": list of field names (CharField/IntegerField
                  with choices) to create "by-label" autocomplete views.
                - "value_fields": list of field names for "by-value"
                  autocomplete views.
                - "record_models": list of related model classes to create
                  generic search autocomplete views.

            Example:
                overrides = {
                    "Book": {
                        "label_fields": ["genre"],
                        "value_fields": ["isbn"],
                        "record_models": [Author, Publisher],
                    }
                }

    Returns:
        tuple:
            - autocomplete_urls (list):
                A list of `django.urls.path` instances defining URL patterns
                for all generated autocomplete views. These should be included
                in the app's `urls.py`.
            - autocomplete_widgets (dict):
                A nested dict of widgets, keyed by model name and field name,
                for use in forms or admin definitions. Example:

                    {
                        "Book": {
                            "genre": partial(ListSelect2, ...),
                            "author": partial(ModelSelect2, ...),
                        },
                        "Author": {...},
                    }

    Usage:
        In your app's `views.py`:

            from core.utils.autocompletion.AutocompletesGeneration import register_autocomplete

            autocomplete_urls, autocomplete_widgets = register_autocomplete(
                overrides={
                    "Book": {
                        "label_fields": ["genre"],
                        "record_models": [Author],
                    }
                }
            )

        In your app's `urls.py`:

            from .autocomplete_views import autocomplete_urls

            app_name = "myapp_autocomplete"
            urlpatterns = autocomplete_urls

    Notes:
        - Dynamically generated view classes are injected into the calling
          module's namespace via `globals()`.
        - M2M fields are not handled here (use Django admin's `filter_horizontal` or similar).
        - If a model has no matching fields, it will simply be skipped.
    """

    overrides = overrides or {}
    app_config = get_calling_app_config()
    if not app_config:
        raise RuntimeError("Could not determine calling app")

    autocomplete_urls = []
    autocomplete_widgets = {}

    for model in app_config.get_models():
        widgets = {}
        app_label = app_config.label
        model_name = model.__name__

        config = overrides.get(model_name, {})

        # use overrides if provided, otherwise build defaults
        label_fields = config.get("label_fields") or [
            f.name
            for f in model._meta.fields
            if isinstance(f, (CharField, IntegerField))
            and getattr(f, "choices", None)
        ]

        value_fields = config.get("value_fields") or []

        record_models = config.get("record_models") or [
            f.related_model
            for f in model._meta.fields
            if getattr(f, "related_model", None) is not None
        ]
        record_models.append(model)

        # Label fields
        for field in label_fields:
            view_name = f"{field.title().replace('_','')}Autocomplete"
            view_class = type(
                view_name,
                (FieldChoicesAutocompleteByLabel,),
                {"model": model, "field_name": field},
            )
            globals()[view_name] = view_class
            url_name = f"{kebabcase(model_name)}-{kebabcase(field)}-by-label-autocomplete"
            autocomplete_urls.append(
                path(f"{url_name}/", view_class.as_view(), name=url_name)
            )
            widgets[field] = partial(
                autocomplete.ListSelect2,
                url=f"{app_label}_autocomplete:{url_name}",
            )

        # Value fields
        for field in value_fields:
            view_name = f"{field.title().replace('_','')}Autocomplete"
            view_class = type(
                view_name,
                (FieldChoicesAutocompleteByValue,),
                {"model": model, "field_name": field},
            )
            globals()[view_name] = view_class
            url_name = f"{kebabcase(model_name)}-{kebabcase(field)}-by-value-autocomplete"
            autocomplete_urls.append(
                path(f"{url_name}/", view_class.as_view(), name=url_name)
            )
            widgets[field] = partial(
                func=autocomplete.ListSelect2,
                url=f"{app_label}_autocomplete:{url_name}",
            )

        # Related models
        for related_model in record_models:
            view_name = f"{related_model.__name__}Autocomplete"
            view_class = type(
                view_name,
                (StrMatchingAutocomplete,),
                {"model": related_model, "__module__": __name__},
            )
            globals()[view_name] = view_class
            url_name = (
                f"{kebabcase(related_model.__name__)}-records-autocomplete"
            )
            autocomplete_urls.append(
                path(f"{url_name}/", view_class.as_view(), name=url_name)
            )

            # attach ModelSelect2 widgets for FK fields pointing to this model
            for field in model._meta.fields:
                if getattr(field, "related_model", None) == related_model:
                    widgets[field.name] = partial(
                        autocomplete.ModelSelect2,
                        url=f"{app_label}_autocomplete:{url_name}",
                    )

        autocomplete_widgets.update({model_name: widgets})

    return autocomplete_urls, autocomplete_widgets


def build_widgets(widget_factories):
    return {field: factory() for field, factory in widget_factories.items()}


def add_model_name(model, dictionary, key):
    if hasattr(model, "_meta"):
        dictionary[key] = f"{model._meta.app_label}.{model.__name__}"
