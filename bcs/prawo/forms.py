from django import forms
from .models import Podmiot, RelacjaPrawna, Rola, Struktura
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets


class PodmiotForm(forms.ModelForm):
    class Meta:
        model = Podmiot
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets["Podmiot"])


class RelacjaPrawnaForm(forms.ModelForm):
    class Meta:
        model = RelacjaPrawna
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets["RelacjaPrawna"])


class RolaForm(forms.ModelForm):
    class Meta:
        model = Rola
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets["Rola"])


class StrukturaForm(forms.ModelForm):
    class Meta:
        model = Struktura
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets["Struktura"])
