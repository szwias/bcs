from django import forms
from dal import autocomplete
from .models import *
from .views import autocomplete_widgets, build_widgets

class MiejsceForm(forms.ModelForm):
    class Meta:
        model = Miejsce
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets['Miejsce'])

class ZdarzenieForm(forms.ModelForm):
    class Meta:
        model = Zdarzenie
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets['Zdarzenie'])
        widgets.update({'miejsce': autocomplete.ModelSelect2(url='kronika_autocomplete:custom-miejsce-from-wydarzenie-to-zdarzenie-autocomplete', forward=['wydarzenie'])})

class ZdarzenieInlineForm(forms.ModelForm):
    class Meta:
        model = Zdarzenie
        fields = ["nazwa", "data", "godzina", "miejsce"]
        widgets = {'miejsce': autocomplete.ModelSelect2(url='kronika_autocomplete:custom-miejsce-from-wydarzenie-to-zdarzenie-autocomplete', forward=['wydarzenie'])}

class ObrazZdarzenieForm(forms.ModelForm):
    class Meta:
        model = ObrazZdarzenie
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets['ObrazZdarzenie'])

class WydarzenieForm(forms.ModelForm):
    class Meta:
        model = Wydarzenie
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets['Wydarzenie'])

class ObrazWydarzenieForm(forms.ModelForm):
    class Meta:
        model = ObrazWydarzenie
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets['ObrazWydarzenie'])

class ProcesForm(forms.ModelForm):
    class Meta:
        model = Proces
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets['Proces'])



