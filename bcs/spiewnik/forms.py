from django import forms
from dal import autocomplete

from .models import KategoriaPiosenki, Piosenka
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets


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
