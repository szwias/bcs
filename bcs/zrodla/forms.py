from django import forms
from django.apps import apps
from core.forms import create_model_forms
from .model_imports import *
from .views import autocomplete_widgets
from core.autocompletion.registry import build_widgets
from osoby.models_dict import names as osoby
from osoby.models import Byt


class EdyktForm(forms.ModelForm):
    class Meta:
        model = Edykt
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets["Edykt"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["autorzy"].queryset = Byt.objects.instance_of(
            apps.get_model(osoby["Czlonek"]), apps.get_model(osoby["Zarzad"])
        )


class UkazForm(forms.ModelForm):
    class Meta:
        model = Ukaz
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets["Ukaz"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["autorzy"].queryset = Byt.objects.instance_of(
            apps.get_model(osoby["Czlonek"]), apps.get_model(osoby["Zarzad"])
        )

model_forms = create_model_forms(autocomplete_widgets)
