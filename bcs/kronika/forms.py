from core.autocompletion.registry import build_widgets
from django import forms
from .model_imports import *
from .views import autocomplete_widgets


class KadencjaForm(forms.ModelForm):
    class Meta:
        model = Kadencja
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Kadencja.__name__])


class KategoriaZadaniaChrzcielnegoForm(forms.ModelForm):
    class Meta:
        model = KategoriaZadaniaChrzcielnego
        fields = "__all__"
        widgets = build_widgets(
            autocomplete_widgets[KategoriaZadaniaChrzcielnego.__name__]
        )


class PodsumowanieKadencjiForm(forms.ModelForm):
    class Meta:
        model = PodsumowanieKadencji
        fields = "__all__"
        widgets = build_widgets(
            autocomplete_widgets[PodsumowanieKadencji.__name__]
        )


class TypWydarzeniaHistorycznegoForm(forms.ModelForm):
    class Meta:
        model = TypWydarzeniaHistorycznego
        fields = "__all__"
        widgets = build_widgets(
            autocomplete_widgets[TypWydarzeniaHistorycznego.__name__]
        )


class WydarzenieHistoryczneForm(forms.ModelForm):
    class Meta:
        model = WydarzenieHistoryczne
        fields = "__all__"
        widgets = build_widgets(
            autocomplete_widgets[WydarzenieHistoryczne.__name__]
        )


class ZadanieChrzcielneForm(forms.ModelForm):
    class Meta:
        model = ZadanieChrzcielne
        fields = "__all__"
        widgets = build_widgets(
            autocomplete_widgets[ZadanieChrzcielne.__name__]
        )
