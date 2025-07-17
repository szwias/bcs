from django import forms
from .models import TradycjaBCS, TradycjaInnegoBractwa, Bractwo, Pojecie, Powiedzenie, Zwyczaj, Zrodlo
from .views import autocomplete_widgets, build_widgets

class BractwoForm(forms.ModelForm):
    class Meta:
        model = Bractwo
        fields = '__all__'

        widgets = build_widgets(autocomplete_widgets['Bractwo'])

class PojecieForm(forms.ModelForm):
    class Meta:
        model = Pojecie
        fields = '__all__'

        widgets = build_widgets(autocomplete_widgets['Pojecie'])

class PowiedzienieForm(forms.ModelForm):
    class Meta:
        model = Powiedzenie
        fields = '__all__'

        widgets = build_widgets(autocomplete_widgets['Powiedzenie'])

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

class ZwyczajForm(forms.ModelForm):
    class Meta:
        model = Zwyczaj
        fields = '__all__'

        widgets = build_widgets(autocomplete_widgets['Zwyczaj'])

class ZrodloForm(forms.ModelForm):
    class Meta:
        model = Zrodlo
        fields = '__all__'

        widgets = build_widgets(autocomplete_widgets['Zrodlo'])

