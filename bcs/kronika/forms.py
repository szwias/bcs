from django import forms
from dal import autocomplete
from .models import *
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets


class CharakterystykaDzialanZarzaduForm(forms.ModelForm):
    class Meta:
        model = CharakterystykaDzialanZarzadu
        fields = "__all__"
        widgets = build_widgets(
            autocomplete_widgets[CharakterystykaDzialanZarzadu.__name__]
        )
