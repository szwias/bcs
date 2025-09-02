from django import forms
from .views import autocomplete_widgets
from core.autocompletion.registry import build_widgets
from .model_imports import *


class ObrazWydarzenieForm(forms.ModelForm):
    class Meta:
        model = ObrazWydarzenie
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[ObrazWydarzenie.__name__])


class ObrazZdarzenieForm(forms.ModelForm):
    class Meta:
        model = ObrazZdarzenie
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[ObrazZdarzenie.__name__])
