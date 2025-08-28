from django import forms
from dal import autocomplete
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets
from .models import (
    Konto,
    Transakcja,
)
from djmoney.forms.fields import MoneyField


class KontoForm(forms.ModelForm):
    class Meta:
        model = Konto
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Konto.__name__])


class TransakcjaForm(forms.ModelForm):
    class Meta:
        model = Transakcja
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Transakcja.__name__])
