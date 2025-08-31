from django import forms
from .models import *
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets


class CzapkaForm(forms.ModelForm):
    class Meta:
        model = Czapka
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Czapka.__name__])


class RodzajCzapkiForm(forms.ModelForm):
    class Meta:
        model = RodzajCzapki
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[RodzajCzapki.__name__])
