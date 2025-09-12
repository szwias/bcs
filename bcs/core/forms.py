import sys

from django.forms import ModelForm

from core.autocompletion.registry import build_widgets
from core.apps import get_calling_app_config


def create_model_forms(autocomplete_widgets=None):
    """
    Create ModelForm classes for all models in the calling app.

    Existing forms in the app's forms.py are reused. Widgets can be customized
    via the optional autocomplete_widgets dictionary.

    Args:
        autocomplete_widgets (dict, optional): Field widget configurations per model. Defaults to None.

    Returns:
        dict: Mapping of form class names to ModelForm classes.

    Raises:
        RuntimeError: If the calling app cannot be determined.
    """
    autocomplete_widgets = autocomplete_widgets or {}
    app_config = get_calling_app_config()
    if not app_config:
        raise RuntimeError("Could not determine calling app")

    # Get the module of the caller
    caller_module = sys.modules[app_config.name + ".forms"]

    model_forms = {}

    for _model in app_config.get_models():
        form_name = f"{_model.__name__}Form"

        # Skip if form already exists in forms.py
        if hasattr(caller_module, form_name):
            form_class = getattr(caller_module, form_name)
            model_forms[form_name] = form_class
            continue

        class Meta:
            model = _model
            fields = "__all__"
            widgets = build_widgets(
                autocomplete_widgets.get(model.__name__, {})
            )

        form_class = type(form_name, (ModelForm,), {"Meta": Meta})
        model_forms[form_name] = form_class

    return model_forms
