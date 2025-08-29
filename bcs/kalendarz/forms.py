from django import forms
from dal import autocomplete

from .models import (
    Chrzest,
    TypWydarzenia,
    TypWyjazdu,
    Wydarzenie,
    WydarzenieKalendarzowe,
    Zdarzenie,
)
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets


class ChrzestForm(forms.ModelForm):
    class Meta:
        model = Chrzest
        fields = "__all__"
        widgets = build_widgets(
            autocomplete_widgets[Chrzest.__name__]
        )


class ZdarzenieForm(forms.ModelForm):
    class Meta:
        model = Zdarzenie
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Zdarzenie.__name__])
        widgets.update(
            {
                "miejsce": autocomplete.ModelSelect2(
                    url="kalendarz_autocomplete:custom-miejsce-from-wydarzenie-to-zdarzenie-autocomplete",
                    forward=["wydarzenie"],
                )
            }
        )


class ZdarzenieInlineForm(forms.ModelForm):
    class Meta:
        model = Zdarzenie
        fields = ["nazwa", "data", "godzina", "miejsce", "powiazane_osoby"]
        widgets = {
            "miejsce": autocomplete.ModelSelect2(
                url="miejsca_autocomplete:miejsce-records-autocomplete",
                forward=["wydarzenie"],
            )
        }

    def __init__(self, *args, **kwargs):
        parent_obj = kwargs.pop("parent_obj")
        super().__init__(*args, **kwargs)
        if (
            parent_obj
            and not self.instance.pk
            and not self.initial.get("data")
        ):
            self.initial["data"] = parent_obj.data_rozpoczecia


class WydarzenieKalendarzoweForm(forms.ModelForm):
    class Meta:
        model = WydarzenieKalendarzowe
        fields = "__all__"
        widgets = build_widgets(
            autocomplete_widgets[WydarzenieKalendarzowe.__name__]
        )


class WydarzenieForm(forms.ModelForm):
    class Meta:
        model = Wydarzenie
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Wydarzenie.__name__])

    def clean(self):
        cd = super().clean()

        if cd.get("czy_jednodniowe"):
            cd["data_zakonczenia"] = cd["data_rozpoczecia"]

        ctw = cd.get("czy_to_wyjazd")

        if not cd.get("typ_wydarzenia") or ctw:
            cd["typ_wydarzenia"] = TypWydarzenia.get_not_applicable_typ()

        if not cd.get("typ_wyjazdu") or not ctw:
            cd["typ_wyjazdu"] = TypWyjazdu.get_not_applicable_typ()

        return cd


class TypWydarzeniaForm(forms.ModelForm):
    class Meta:
        model = TypWydarzenia
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[TypWydarzenia.__name__])


class TypWyjazduForm(forms.ModelForm):
    class Meta:
        model = TypWyjazdu
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[TypWyjazdu.__name__])
