from django import forms
from dal import autocomplete
from .models import *
from .views import autocomplete_widgets, build_widgets
from django.contrib.postgres.forms import SimpleArrayField

class CzapkaForm(forms.ModelForm):
    class Meta:
        model = Czapka
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Start: Wydzial initially empty
        self.fields['wydzial'].choices = []

        uczelnia = None
        if 'uczelnia' in self.data:
            uczelnia = self.data.get('uczelnia')
        elif self.instance and self.instance.uczelnia:
            uczelnia = self.instance.uczelnia

        if uczelnia in Czapka.WydzialChoices:
            wydzial_choices = Czapka.WydzialChoices[uczelnia]
            self.fields['wydzial'].choices = wydzial_choices
            self.fields['wydzial'].widget = forms.Select(choices=wydzial_choices)

class CzlonekForm(forms.ModelForm):
    class Meta:
        model = Czlonek
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets['Czlonek'])

    przezwiska = SimpleArrayField(
        base_field=forms.CharField(),
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 50}),
        delimiter=','
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields['czapka_1'].initial = Czapka.get_dont_know_czapka()
            self.fields['czapka_2'].initial = Czapka.get_not_applicable_czapka()
            self.fields['rodzic_1'].initial = Czlonek.get_dont_know_czlonek()

    def clean(self):
        cd = super().clean()

        status = cd.get('status')

        if status in [Czlonek.Status.CZLONEK, Czlonek.Status.WETERAN]:
            cd['ochrzczony'] = TextChoose.YES[0]

        ochrzczony = cd.get('ochrzczony')

        if ochrzczony == TextChoose.NO[0]:
            cd['rok_chrztu'] = IntAlt.NOT_APPLICABLE[0]
        elif ochrzczony == TextAlt.DONT_KNOW[0]:
            cd['rok_chrztu'] = IntAlt.DONT_KNOW[0]

        rok_chrztu = cd.get('rok_chrztu')
        if rok_chrztu in [IntAlt.NOT_APPLICABLE[0], IntAlt.DONT_KNOW[0]]:
            cd['miesiac_chrztu'] = rok_chrztu

        miesiac_chrztu = cd.get('miesiac_chrztu')
        if miesiac_chrztu in [IntAlt.NOT_APPLICABLE[0], IntAlt.DONT_KNOW[0]]:
            cd['dzien_chrztu'] = miesiac_chrztu

        imie_piwne_1 = cd.get('imie_piwne_1')
        if imie_piwne_1 not in ["Nie wiem", "Nie dotyczy"]:
            cd['imie_piwne_1_wybor'] = "other"

        imie_piwne_2 = cd.get('imie_piwne_2')
        if imie_piwne_2 not in ["Nie wiem", "Nie dotyczy"]:
            cd['imie_piwne_2_wybor'] = "other"

        imie_piwne_1_wybor = cd.get('imie_piwne_1_wybor')
        if imie_piwne_1_wybor != "other":
            if imie_piwne_1_wybor == TextAlt.DONT_KNOW[0]:
                cd['imie_piwne_1'] = TextAlt.DONT_KNOW[1]
            elif imie_piwne_1_wybor == TextAlt.NOT_APPLICABLE[0]:
                cd['imie_piwne_1'] = TextAlt.NOT_APPLICABLE[1]
            cd['imie_piwne_2_wybor'] = TextAlt.NOT_APPLICABLE[0]
            cd['imie_piwne_2'] = TextAlt.NOT_APPLICABLE[1]

        staz = cd.get('staz')
        if staz == Czas.ROK_ZALOZENIA:
            cd['pewnosc_stazu'] = "T"

        rodzic_1 = cd.get('rodzic_1')
        rodzic_2 = cd.get('rodzic_2')

        if not rodzic_1:
            cd["rodzic_1"] = Czlonek.get_dont_know_czlonek()
        if rodzic_1 == Czlonek.get_not_applicable_czlonek():
            cd["rodzic_2"] = Czlonek.get_not_applicable_czlonek()

        if not rodzic_2:
            cd["rodzic_2"] = Czlonek.get_not_applicable_czlonek()

        return cd

class BeanForm(forms.ModelForm):
    class Meta:
        model = Bean
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets['Bean'])

    przezwiska = SimpleArrayField(
        base_field=forms.CharField(),
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 50}),
        delimiter=','
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields['czapka_1'].initial = Czapka.get_dont_know_czapka()
            self.fields['czapka_2'].initial = Czapka.get_not_applicable_czapka()
            self.fields['rodzic_1'].initial = Czlonek.get_not_applicable_czlonek()
            self.fields['rodzic_2'].initial = Czlonek.get_not_applicable_czlonek()

class OsobyForm(forms.ModelForm):
    class Meta:
        model = Osoby
        exclude = ['content_type', 'object_id']
        widgets = {
            'czlonek': autocomplete.ModelSelect2(
                url='czlonkowie:czlonek-records-autocomplete'
            ),
            'bean': autocomplete.ModelSelect2(
                url='czlonkowie:bean-records-autocomplete'
            ),
            'inna_osoba': autocomplete.ModelSelect2(
                url='czlonkowie:inna-osoba-records-autocomplete'
            )
        }

class ImieSzlacheckieForm(forms.ModelForm):
    posiadacz_display = forms.CharField(
        label="Posiadacz",
        required=False,
        disabled=True,
    )

    class Meta:
        model = ImieSzlacheckie
        fields = ['imie', 'posiadacz_display']
        widgets = build_widgets(autocomplete_widgets['ImieSzlacheckie'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.nazwa:
            imie = self.instance.nazwa
            self.fields['posiadacz_display'].initial = f"{imie.nazwa} {imie.nazwisko}"

class ZwierzeCzapkoweForm(forms.ModelForm):
    imie_display = forms.CharField(
        label="Imię czapkowe",
        required=False,
        disabled=True,
    )

    class Meta:
        model = ZwierzeCzapkowe
        fields = ['czlonek', 'imie_display', 'zwierze', 'wyjasnienie']
        widgets = build_widgets(autocomplete_widgets['ZwierzeCzapkowe'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.czlonek:
            czlonek = self.instance.czlonek
            self.fields['imie_display'].initial = f"\"{czlonek.imie_piwne_1}\""

class DawnyZarzadForm(forms.ModelForm):
    class Meta:
        model = DawnyZarzad
        fields = '__all__'

        widgets = build_widgets(autocomplete_widgets['DawnyZarzad'])
        widgets.update({'kadencja': autocomplete.ModelSelect2(url='core:custom-kadencja-autocomplete')})

class ZarzadForm(forms.ModelForm):
    class Meta:
        model = Zarzad
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets['Zarzad'])
        widgets.update({'kadencja': autocomplete.ModelSelect2(url='core:custom-kadencja-autocomplete')})

class WielkiMistrzForm(forms.ModelForm):
    class Meta:
        model = WielkiMistrz
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets['WielkiMistrz'])


class HallOfFameForm(forms.ModelForm):
    class Meta:
        model = HallOfFame
        exclude = ['ordering']
        widgets = build_widgets(autocomplete_widgets['HallOfFame'])

class InnaOsobaForm(forms.ModelForm):
    class Meta:
        model = InnaOsoba
        fields = '__all__'
        widgets = build_widgets(autocomplete_widgets['InnaOsoba'])

        przezwiska = SimpleArrayField(
            base_field=forms.CharField(),
            required=False,
            widget=forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            delimiter=','
        )

