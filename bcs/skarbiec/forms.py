from django import forms
from .views import autocomplete_widgets
from core.autocompletion.registry import build_widgets
from .model_imports import *


class KontoForm(forms.ModelForm):
    class Meta:
        model = Konto
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Konto.__name__])


class TransakcjaForm(forms.ModelForm):
    class Meta:
        model = Transakcja
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Transakcja.__name__])
