from django import forms

from kalendarz.models import Wydarzenie
from .models import (
    Kadencja,
    PodsumowanieKadencji,
    TypWydarzeniaHistorycznego,
    WydarzenieHistoryczne,
    ZadanieChrzcielne,
)
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets


class KadencjaForm(forms.ModelForm):
    class Meta:
        model = Kadencja
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Kadencja.__name__])


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        data_value = self.data.get("data") or self.initial.get("data")

        if data_value:
            self.fields["wydarzenie"].queryset = Wydarzenie.objects.filter(
                data_rozpoczecia=data_value, czy_jednodniowe=True
            )
        else:
            self.fields["wydarzenie"].queryset = Wydarzenie.objects.none()


class ZadanieChrzcielneForm(forms.ModelForm):
    class Meta:
        model = ZadanieChrzcielne
        fields = "__all__"
        widgets = build_widgets(
            autocomplete_widgets[ZadanieChrzcielne.__name__]
        )
