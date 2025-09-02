from django import forms
from .views import autocomplete_widgets
from core.autocompletion.registry import build_widgets
from .model_imports import *


class NagrodzeniForm(forms.ModelForm):
    class Meta:
        model = Nagrodzeni
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Nagrodzeni.__name__])


class OdznaczenieForm(forms.ModelForm):
    class Meta:
        model = Odznaczenie
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Odznaczenie.__name__])
