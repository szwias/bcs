from django import forms
from dal import autocomplete

from miejsca.models import Miejsce
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

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # This will only work when there's a parent instance
            wydarzenie = self.instance.wydarzenie
            if wydarzenie:
                self.fields['miejsce'].queryset = wydarzenie.miejsca.all()
            else:
                # No parent yet (e.g., new Wydarzenie), maybe no filtering or empty
                self.fields['miejsce'].queryset = Miejsce.objects.none()

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

    def clean(self):
        cd = super().clean()

        if not cd.get('typ_wydarzenia'):
            cd['typ_wydarzenia'] = TypWydarzenia.get_not_applicable_typ()

        if not cd.get('typ_wyjazdu'):
            cd['typ_wyjazdu'] = TypWyjazdu.get_not_applicable_typ()

        return cd


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
