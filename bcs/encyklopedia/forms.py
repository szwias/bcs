from django import forms
from .models import Bractwo, GrupaBractw, Pojecie, Powiedzenie, TradycjaBCS, TradycjaInnegoBractwa, Zwyczaj, Zrodlo
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets


class BractwoForm(forms.ModelForm):
    class Meta:
        model = Bractwo
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets[Bractwo.__name__])


class GrupaBractwForm(forms.ModelForm):
    class Meta:
        model = GrupaBractw
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets[GrupaBractw.__name__])


class PojecieForm(forms.ModelForm):
    class Meta:
        model = Pojecie
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets[Pojecie.__name__])


class PowiedzienieForm(forms.ModelForm):
    class Meta:
        model = Powiedzenie
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets[Powiedzenie.__name__])


class TradycjaBCSForm(forms.ModelForm):
    class Meta:
        model = TradycjaBCS
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets[TradycjaBCS.__name__])


class TradycjaInnegoBractwaForm(forms.ModelForm):
    class Meta:
        model = TradycjaInnegoBractwa
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets[TradycjaInnegoBractwa.__name__])


class ZwyczajForm(forms.ModelForm):
    class Meta:
        model = Zwyczaj
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets[Zwyczaj.__name__])


class ZrodloForm(forms.ModelForm):
    class Meta:
        model = Zrodlo
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets[Zrodlo.__name__])
