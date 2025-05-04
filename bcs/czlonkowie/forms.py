from django import forms
from dal import autocomplete
from .models import *
# from .views import autocomplete_widgets

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
        fields = '__all__'  # Or specify the fields you want
        widgets = {
            'rok_chrztu': autocomplete.ListSelect2(url='czlonkowie:czlonek_rok_chrztu_label_autocomplete'),
            'miesiac_chrztu': autocomplete.ListSelect2(url='czlonkowie:czlonek_miesiac_chrztu_label_autocomplete'),
            'dzien_chrztu': autocomplete.ListSelect2(url='czlonkowie:czlonek_dzien_chrztu_label_autocomplete'),
            'staz': autocomplete.ListSelect2(url='czlonkowie:czlonek_staz_label_autocomplete'),
            'status': autocomplete.ListSelect2(url='czlonkowie:czlonek_status_label_autocomplete'),

            'czapka_1': autocomplete.ModelSelect2(url='czlonkowie:czapka_records_autocomplete'),
            'czapka_2': autocomplete.ModelSelect2(url='czlonkowie:czapka_records_autocomplete'),
            'rodzic_1': autocomplete.ModelSelect2(url='czlonkowie:czlonek_records_autocomplete'),
            'rodzic_2': autocomplete.ModelSelect2(url='czlonkowie:czlonek_records_autocomplete'),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields['czapka_1'].initial = Czapka.get_dont_know_czapka()[0]
            self.fields['czapka_2'].initial = Czapka.get_not_applicable_czapka()[0]

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

        imie_piwne_1 = cd.get('imie_piwne_1')
        if imie_piwne_1 not in ["Nie wiem", "Nie dotyczy"]:
            cd['imie_piwne_1_wybor'] = "other"

        imie_piwne_2 = cd.get('imie_piwne_2')
        if imie_piwne_2 not in ["Nie wiem", "Nie dotyczy"]:
            cd['imie_piwne_2_wybor'] = "other"

        staz = cd.get('staz')
        if staz == Czas.ROK_ZALOZENIA:
            cd['pewnosc_stazu'] = True

        return cd

class ImieSzlacheckieForm(forms.ModelForm):
    posiadacz_display = forms.CharField(
        label="Posiadacz",
        required=False,
        disabled=True,
    )

    class Meta:
        model = ImieSzlacheckie
        fields = ['imie', 'posiadacz_display']
        widgets = {
            'imie': autocomplete.ModelSelect2(url='czlonkowie:czlonek-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.imie:
            imie = self.instance.imie
            self.fields['posiadacz_display'].initial = f"{imie.imie} {imie.nazwisko}"

class ZwierzeCzapkoweForm(forms.ModelForm):
    imie_display = forms.CharField(
        label="Imię czapkowe",
        required=False,
        disabled=True,
    )

    class Meta:
        model = ZwierzeCzapkowe
        fields = ['czlonek', 'imie_display', 'zwierze', 'wyjasnienie']
        widgets = {
            'czlonek': autocomplete.ModelSelect2(url='czlonkowie:czlonek-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.czlonek:
            czlonek = self.instance.czlonek
            self.fields['imie_display'].initial = f"\"{czlonek.imie_piwne_1}\""


class DawnyZarzadForm(forms.ModelForm):
    class Meta:
        model = DawnyZarzad
        fields = '__all__'  # Or specify the fields you want
        widgets = {
            'kadencja': autocomplete.ModelSelect2(url='core:kadencja-autocomplete'),

            'wielki_mistrz': autocomplete.ModelSelect2(url='czlonkowie:czlonek-autocomplete'),
            'kasztelan': autocomplete.ModelSelect2(url='czlonkowie:czlonek-autocomplete'),
            'skarbnik': autocomplete.ModelSelect2(url='czlonkowie:czlonek-autocomplete'),
            'bibendi': autocomplete.ModelSelect2(url='czlonkowie:czlonek-autocomplete'),
            'cantandi': autocomplete.ModelSelect2(url='czlonkowie:czlonek-autocomplete'),
            'kontakt_z_SSUJ': autocomplete.ModelSelect2(url='czlonkowie:czlonek-autocomplete'),
            'kontakt_z_SKNHI': autocomplete.ModelSelect2(url='czlonkowie:czlonek-autocomplete'),
        }

class ZarzadForm(forms.ModelForm):
    class Meta:
        model = Zarzad
        fields = '__all__'  # Or specify the fields you want
        widgets = {
            'kadencja': autocomplete.ModelSelect2(url='core:kadencja-autocomplete'),

            'wielki_mistrz': autocomplete.ModelSelect2(url='czlonkowie:czlonek-autocomplete'),
            'kasztelan': autocomplete.ModelSelect2(url='czlonkowie:czlonek-autocomplete'),
            'skarbnik': autocomplete.ModelSelect2(url='czlonkowie:czlonek-autocomplete'),
            'cantandi': autocomplete.ModelSelect2(url='czlonkowie:czlonek-autocomplete'),
            'sekretarz': autocomplete.ModelSelect2(url='czlonkowie:czlonek-autocomplete'),
        }

class WielkiMistrzForm(forms.ModelForm):
    class Meta:
        model = WielkiMistrz
        fields = '__all__'
        widgets = {
            'imie': autocomplete.ModelSelect2(url='czlonkowie:czlonek-autocomplete'),
        }


class HallOfFameForm(forms.ModelForm):
    class Meta:
        model = HallOfFame
        exclude = ['ordering']
        widgets = {
            'czlonek': autocomplete.ModelSelect2(url='core:kadencja-autocomplete'),
        }



