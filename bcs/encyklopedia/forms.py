from django import forms
from dal import autocomplete
from .models import Tradycja
from .views import autocomplete_widgets, build_widgets

class TradycjaForm(forms.ModelForm):
    class Meta:
        model = Tradycja
        fields = '__all__'

        widgets = build_widgets(autocomplete_widgets['Tradycja'])

    def clean(self):
        cd = super().clean()

        rodzaj = cd.get('rodzaj')
        if rodzaj != Tradycja.Authors.BCS:
            cd['okolicznosci_powstania'] = Tradycja.Okolicznosci.INNE

        return cd


