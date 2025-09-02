from django import forms
from .views import autocomplete_widgets
from .model_imports import *
from core.autocompletion.registry import build_widgets


class ZwrotForm(forms.ModelForm):
    class Meta:
        model = Zwrot
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Zwrot.__name__])
