from django import forms
from dal import autocomplete
from .models import TradycjaBCS, TradycjaInnegoBractwa
from .views import autocomplete_widgets, build_widgets

class TradycjaBCSForm(forms.ModelForm):
    class Meta:
        model = TradycjaBCS
        fields = '__all__'

        widgets = build_widgets(autocomplete_widgets['TradycjaBCS'])

    def clean(self):
        cd = super().clean()

        rodzaj = cd.get('rodzaj')
        if rodzaj != TradycjaBCS.Authors.BCS:
            cd['okolicznosci_powstania'] = TradycjaBCS.Okolicznosci.INNE

        return cd

class TradycjaInnegoBractwaForm(forms.ModelForm):
    class Meta:
        model = TradycjaInnegoBractwa
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets['TradycjaInnegoBractwa'])


