from django import forms
from .models import (
    CharakterystykaDzialanZarzadu,
    TypWydarzeniaHistorycznego,
    WydarzenieHistoryczne
)
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets


class CharakterystykaDzialanZarzaduForm(forms.ModelForm):
    class Meta:
        model = CharakterystykaDzialanZarzadu
        fields = "__all__"
        widgets = build_widgets(
            autocomplete_widgets[CharakterystykaDzialanZarzadu.__name__]
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
