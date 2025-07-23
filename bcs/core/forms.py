from django import forms
from core.models import *
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import *


class KadencjaForm(forms.ModelForm):
    class Meta:
        model = Kadencja
        fields = ["rozpoczecie"]
        widgets = build_widgets(autocomplete_widgets[Kadencja.__name__])

    def clean(self):
        cd = super(KadencjaForm, self).clean()
        start = cd.get("rozpoczecie")
        if start is not None:
            self.instance.zakonczenie = start + 1

        return cd
