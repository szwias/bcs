from django import forms
from core.utils.czas.models import *
from .views import autocomplete_widgets
from core.utils.automation.ViewsGeneration import *

class KadencjaForm(forms.ModelForm):
    class Meta:
        model = Kadencja
        fields = ['rozpoczecie']
        widgets = build_widgets(autocomplete_widgets['Kadencja'])

    def clean(self):
        cd = super(KadencjaForm, self).clean()
        start = cd.get('rozpoczecie')
        if start is not None:
            self.instance.zakonczenie = start + 1

        return cd
