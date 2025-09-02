from django import forms

from .model_imports import *
from .views import autocomplete_widgets
from core.autocompletion.registry import build_widgets


class KategoriaPiosenkiForm(forms.ModelForm):
    class Meta:
        model = KategoriaPiosenki
        fields = "__all__"
        widgets = build_widgets(
            autocomplete_widgets[KategoriaPiosenki.__name__]
        )


class PiosenkaForm(forms.ModelForm):
    class Meta:
        model = Piosenka
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Piosenka.__name__])
