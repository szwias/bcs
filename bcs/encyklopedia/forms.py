from django import forms
from .models import (
    Aforyzm,
    Bractwo,
    Cytat,
    GrupaBractw,
    Pojecie,
    TradycjaBCS,
    TradycjaInnegoBractwa,
    Zwyczaj,
)
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets


class AforyzmForm(forms.ModelForm):
    class Meta:
        model = Aforyzm
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Aforyzm.__name__])


class BractwoForm(forms.ModelForm):
    class Meta:
        model = Bractwo
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Bractwo.__name__])


class CytatForm(forms.ModelForm):
    class Meta:
        model = Cytat
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Cytat.__name__])


class GrupaBractwForm(forms.ModelForm):
    class Meta:
        model = GrupaBractw
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[GrupaBractw.__name__])


class PojecieForm(forms.ModelForm):
    class Meta:
        model = Pojecie
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Pojecie.__name__])


class TradycjaBCSForm(forms.ModelForm):
    class Meta:
        model = TradycjaBCS
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[TradycjaBCS.__name__])


class TradycjaInnegoBractwaForm(forms.ModelForm):
    class Meta:
        model = TradycjaInnegoBractwa
        fields = "__all__"
        widgets = build_widgets(
            autocomplete_widgets[TradycjaInnegoBractwa.__name__]
        )


class ZwyczajForm(forms.ModelForm):
    class Meta:
        model = Zwyczaj
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Zwyczaj.__name__])
