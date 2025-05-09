from django import forms
from dal import autocomplete
from .models import *
from .views import autocomplete_widgets, build_widgets

class TradycjaForm(forms.ModelForm):
    class Meta:
        model = Tradycja
        fields = '__all__'

        widgets = build_widgets(autocomplete_widgets['Tradycja'])
