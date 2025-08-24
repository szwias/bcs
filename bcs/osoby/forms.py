from django import forms
from dal import autocomplete
from .models import *
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets
from django.contrib.postgres.forms import SimpleArrayField


class DawnyZarzadForm(forms.ModelForm):
    class Meta:
        model = DawnyZarzad
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[DawnyZarzad.__name__])


class HallOfFameForm(forms.ModelForm):
    class Meta:
        model = HallOfFame
        exclude = ["ordering"]
        widgets = build_widgets(autocomplete_widgets[HallOfFame.__name__])


class ImieSzlacheckieForm(forms.ModelForm):
    posiadacz_display = forms.CharField(
        label="Posiadacz",
        required=False,
        disabled=True,
    )

    class Meta:
        model = ImieSzlacheckie
        fields = ["imie", "posiadacz_display"]
        widgets = build_widgets(autocomplete_widgets[ImieSzlacheckie.__name__])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.imie:
            imie = self.instance.imie
            self.fields["posiadacz_display"].initial = (
                f"{imie.imie} {imie.nazwisko}"
            )


class KomisjaRewizyjnaForm(forms.ModelForm):
    class Meta:
        model = KomisjaRewizyjna
        fields = "__all__"
        widgets = build_widgets(
            autocomplete_widgets[KomisjaRewizyjna.__name__]
        )


class NowyZarzadForm(forms.ModelForm):
    class Meta:
        model = NowyZarzad
        fields = [
            "kadencja",
            "wielki_mistrz",
            "kasztelan",
            "skarbnik",
            "sekretarz",
            "cantandi",
        ]
        widgets = build_widgets(autocomplete_widgets[NowyZarzad.__name__])


# OsobaForm Family
# ----------------------------------------------
class OsobaForm(forms.ModelForm):
    class Meta:
        model = Osoba
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets["Osoba"])

    przezwiska = SimpleArrayField(
        base_field=forms.CharField(),
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "cols": 50}),
        delimiter=",",
    )


class BeanForm(OsobaForm):
    class Meta:
        model = Bean
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Bean.__name__])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields["czapka_1"].initial = Czapka.get_dont_know_czapka()
            self.fields["czapka_2"].initial = (
                Czapka.get_not_applicable_czapka()
            )
            self.fields["rodzic_1"].initial = (
                Czlonek.get_not_applicable_czlonek()
            )
            self.fields["rodzic_2"].initial = (
                Czlonek.get_not_applicable_czlonek()
            )


class CzlonekForm(OsobaForm):
    class Meta:
        model = Czlonek
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets["Czlonek"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields["czapka_1"].initial = Czapka.get_dont_know_czapka()
            self.fields["czapka_2"].initial = (
                Czapka.get_not_applicable_czapka()
            )
            self.fields["rodzic_1"].initial = Czlonek.get_dont_know_czlonek()
            self.fields["rodzic_2"].initial = (
                Czlonek.get_not_applicable_czlonek()
            )

    def clean(self):
        cd = super().clean()

        status = cd.get("status")

        if status in [Czlonek.Status.CZLONEK, Czlonek.Status.WETERAN]:
            cd["ochrzczony"] = TextChoose.YES[0]

        ochrzczony = cd.get("ochrzczony")

        if ochrzczony == TextChoose.NO[0]:
            cd["rok_chrztu"] = IntAlt.NOT_APPLICABLE[0]
        elif ochrzczony == TextAlt.DONT_KNOW[0]:
            cd["rok_chrztu"] = IntAlt.DONT_KNOW[0]

        rok_chrztu = cd.get("rok_chrztu")
        if rok_chrztu in [IntAlt.NOT_APPLICABLE[0], IntAlt.DONT_KNOW[0]]:
            cd["miesiac_chrztu"] = rok_chrztu

        miesiac_chrztu = cd.get("miesiac_chrztu")
        if miesiac_chrztu in [IntAlt.NOT_APPLICABLE[0], IntAlt.DONT_KNOW[0]]:
            cd["dzien_chrztu"] = miesiac_chrztu

        imie_piwne_1 = cd.get("imie_piwne_1")
        if imie_piwne_1 not in ["Nie wiem", "Nie dotyczy"]:
            cd["imie_piwne_1_wybor"] = "other"

        imie_piwne_2 = cd.get("imie_piwne_2")
        if imie_piwne_2 not in ["Nie wiem", "Nie dotyczy"]:
            cd["imie_piwne_2_wybor"] = "other"

        imie_piwne_1_wybor = cd.get("imie_piwne_1_wybor")
        if imie_piwne_1_wybor != "other":
            if imie_piwne_1_wybor == TextAlt.DONT_KNOW[0]:
                cd["imie_piwne_1"] = TextAlt.DONT_KNOW[1]
            elif imie_piwne_1_wybor == TextAlt.NOT_APPLICABLE[0]:
                cd["imie_piwne_1"] = TextAlt.NOT_APPLICABLE[1]
            cd["imie_piwne_2_wybor"] = TextAlt.NOT_APPLICABLE[0]
            cd["imie_piwne_2"] = TextAlt.NOT_APPLICABLE[1]

        staz = cd.get("staz")
        if staz == Czas.ROK_ZALOZENIA:
            cd["pewnosc_stazu"] = "T"

        rodzic_1 = cd.get("rodzic_1")
        rodzic_2 = cd.get("rodzic_2")

        if not rodzic_1:
            cd["rodzic_1"] = Czlonek.get_dont_know_czlonek()
        if rodzic_1 == Czlonek.get_not_applicable_czlonek():
            cd["rodzic_2"] = Czlonek.get_not_applicable_czlonek()

        if not rodzic_2:
            cd["rodzic_2"] = Czlonek.get_not_applicable_czlonek()

        return cd


class InnaOsobaForm(OsobaForm):
    class Meta:
        model = InnaOsoba
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[InnaOsoba.__name__])


# ---------------------------------------------- END


class WielkiMistrzForm(forms.ModelForm):
    class Meta:
        model = WielkiMistrz
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[WielkiMistrz.__name__])


class ZwierzeCzapkoweForm(forms.ModelForm):
    imie_display = forms.CharField(
        label="Imię czapkowe",
        required=False,
        disabled=True,
    )

    class Meta:
        model = ZwierzeCzapkowe
        fields = ["czlonek", "imie_display", "zwierze", "wyjasnienie"]
        widgets = build_widgets(autocomplete_widgets[ZwierzeCzapkowe.__name__])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.czlonek:
            czlonek = self.instance.czlonek
            self.fields["imie_display"].initial = f'"{czlonek.imie_piwne_1}"'
