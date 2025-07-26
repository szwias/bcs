from django import forms
from dal import autocomplete
from .views import autocomplete_widgets
from .models import Zwrot
from core.utils.autocompletion.AutocompletesGeneration import build_widgets


class ZwrotForm(forms.ModelForm):
    class Meta:
        model = Zwrot
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Zwrot.__name__])
