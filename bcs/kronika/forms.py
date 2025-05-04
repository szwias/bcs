from django import forms
from dal import autocomplete
from .models import *

class WydarzenieForm(forms.ModelForm):
    class Meta:
        model = Wydarzenie
        fields = '__all__'
        widgets = {
            'typ': autocomplete.ListSelect2(url='kronika:typ-wydarzenia-autocomplete'),

            'miejsce': autocomplete.ModelSelect2(url='kronika:miejsce-autocomplete'),
            'zdarzenia': autocomplete.ModelSelect2(url='kronika:zdarzenie-autocomplete'),
        }

class WyjazdForm(forms.ModelForm):
    class Meta:
        model = Wyjazd
        fields = '__all__'
        widgets = {
            'typ': autocomplete.ListSelect2(url='kronika:typ-wyjazdu-autocomplete'),

            'miejsce': autocomplete.ModelSelect2(url='kronika:miejsce-autocomplete'),
            'zdarzenie': autocomplete.ModelSelect2(url='kronika:zdarzenie-autocomplete'),
        }

class MiejsceForm(forms.ModelForm):
    class Meta:
        model = Miejsce
        fields = '__all__'
        widgets = {
            'typ': autocomplete.ListSelect2(url='kronika:typ-miejsca-autocomplete'),
        }

class ZdarzenieForm(forms.ModelForm):
    class Meta:
        model = Wydarzenie
        fields = '__all__'

class ProcesForm(forms.ModelForm):
    class Meta:
        model = Proces
        fields = '__all__'