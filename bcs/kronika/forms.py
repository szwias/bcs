from django import forms
from dal import autocomplete
from .models import *
from .views import autocomplete_widgets
from core.utils.automation.AutocompletesGeneration import build_widgets


class ZdarzenieForm(forms.ModelForm):
    class Meta:
        model = Zdarzenie
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets[Zdarzenie.__name__])
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
        widgets = build_widgets(autocomplete_widgets[ObrazZdarzenie.__name__])


class WydarzenieForm(forms.ModelForm):
    class Meta:
        model = Wydarzenie
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets[Wydarzenie.__name__])


class ObrazWydarzenieForm(forms.ModelForm):
    class Meta:
        model = ObrazWydarzenie
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets[ObrazWydarzenie.__name__])


class ProcesForm(forms.ModelForm):
    class Meta:
        model = Proces
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets[Proces.__name__])


class CharakterystykaDzialanZarzaduForm(forms.ModelForm):
    class Meta:
        model = CharakterystykaDzialanZarzadu
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets[CharakterystykaDzialanZarzadu.__name__])


class TypWydarzeniaForm(forms.ModelForm):
    class Meta:
        model = TypWydarzenia
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets[TypWydarzenia.__name__])


class TypWyjazduForm(forms.ModelForm):
    class Meta:
        model = TypWyjazdu
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets[TypWyjazdu.__name__])
