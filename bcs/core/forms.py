from django import forms
from dal import autocomplete
from core.utils.czas.models import *

class KadencjaForm(forms.ModelForm):
    class Meta:
        model = Kadencja
        fields = ['rozpoczecie']
        widgets = {
            'rozpoczecie': autocomplete.ListSelect2(url='core:rozpoczecie-autocomplete'),
        }

    def clean(self):
        cd = super(KadencjaForm, self).clean()
        start = cd.get('rozpoczecie')
        if start is not None:
            self.instance.zakonczenie = start + 1

        return cd
