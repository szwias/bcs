from django import forms
from dal import autocomplete
from .models import *
from .views import autocomplete_widgets
from core.utils.automation.AutocompletesGeneration import build_widgets

class KrajForm(forms.ModelForm):
    class Meta:
        model = Kraj
        fields = '__all__'

        # widgets = build_widgets(autocomplete_widgets['Kraj'])

class UczelniaForm(forms.ModelForm):
    class Meta:
        model = Uczelnia
        fields = '__all__'

        widgets = build_widgets(autocomplete_widgets['Uczelnia'])

class WydzialForm(forms.ModelForm):
    class Meta:
        model = Wydzial
        fields = '__all__'

        widgets = build_widgets(autocomplete_widgets['Wydzial'])