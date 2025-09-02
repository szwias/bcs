from django.forms import ModelForm
from core.autocompletion.registry import build_widgets
from core.apps import get_calling_app_config


def create_modelforms(autocomplete_widgets=None):
    app_config = get_calling_app_config()
    forms = {}

    autocomplete_widgets = autocomplete_widgets or {}

    for _model in app_config.get_models():
        class Meta:
            model = _model
            fields = "__all__"
            widgets = build_widgets(
                autocomplete_widgets.get(_model.__name__, {})
            )

        form_class = type(
            f"{_model.__name__}Form",
            (ModelForm,),
            {"Meta": Meta}
        )
        forms[_model.__name__ + "Form"] = form_class

    return forms

