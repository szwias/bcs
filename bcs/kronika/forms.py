from django import forms
from dal import autocomplete
from .models import *
from .views import autocomplete_widgets, build_widgets

class MiejsceForm(forms.ModelForm):
    class Meta:
        model = Miejsce
        fields = '__all__'

class UczestnictwoForm(forms.ModelForm):
    class Meta:
        model = Uczestnictwo
        fields = '__all__'
        widgets = {
            'czlonek': autocomplete.ModelSelect2(
                url='czlonkowie:czlonek-records-autocomplete'
            ),
        }

class WydarzenieForm(forms.ModelForm):
    class Meta:
        model = Wydarzenie
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets['Wydarzenie'])

class ProcesForm(forms.ModelForm):
    class Meta:
        model = Proces
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets['Proces'])

class WyjazdForm(forms.ModelForm):
    class Meta:
        model = Wyjazd
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets['Wyjazd'])



