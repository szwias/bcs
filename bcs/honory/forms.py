from django import forms
from dal import autocomplete
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets
from .models import *


class NagrodzeniForm(forms.ModelForm):
    class Meta:
        model = Nagrodzeni
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Nagrodzeni.__name__])


class OdznaczenieForm(forms.ModelForm):
    class Meta:
        model = Odznaczenie
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Odznaczenie.__name__])
