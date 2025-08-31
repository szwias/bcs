from django import forms
from .models import (
    DlugoscKadencji,
    Podmiot,
    PrawoObowiazek,
    RelacjaPrawna,
    Rola,
    Struktura,
    WielkoscStruktury,
)
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets


class DlugoscKadencjiForm(forms.ModelForm):
    class Meta:
        model = DlugoscKadencji
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[DlugoscKadencji.__name__])


class PodmiotForm(forms.ModelForm):
    class Meta:
        model = Podmiot
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Podmiot.__name__])


class PrawoObowiazekForm(forms.ModelForm):
    class Meta:
        model = PrawoObowiazek
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[PrawoObowiazek.__name__])


class RelacjaPrawnaForm(forms.ModelForm):
    class Meta:
        model = RelacjaPrawna
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[RelacjaPrawna.__name__])


class RolaForm(forms.ModelForm):
    class Meta:
        model = Rola
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Rola.__name__])


class StrukturaForm(forms.ModelForm):
    class Meta:
        model = Struktura
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Struktura.__name__])


class WielkoscStrukturyForm(forms.ModelForm):
    class Meta:
        model = WielkoscStruktury
        fields = "__all__"
        widgets = build_widgets(
            autocomplete_widgets[WielkoscStruktury.__name__]
        )
