from django import forms
from django.apps import apps

from .model_imports import *
from .views import autocomplete_widgets
from core.autocompletion.registry import build_widgets
from osoby.models_dict import names as osoby
from osoby.models import Byt


class DokumentForm(forms.ModelForm):
    class Meta:
        model = Dokument
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets["Dokument"])


class EdyktForm(forms.ModelForm):
    class Meta:
        model = Edykt
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets["Edykt"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["autorzy"].queryset = Byt.objects.instance_of(
            apps.get_model(osoby["Czlonek"]), apps.get_model(osoby["Zarzad"])
        )


class KorespondencjaForm(forms.ModelForm):
    class Meta:
        model = Korespondencja
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Korespondencja.__name__])


class OswiadczenieForm(forms.ModelForm):
    class Meta:
        model = Oswiadczenie
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Oswiadczenie.__name__])


class RozliczenieForm(forms.ModelForm):
    class Meta:
        model = Rozliczenie
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Rozliczenie.__name__])


class UchwalaForm(forms.ModelForm):
    class Meta:
        model = Uchwala
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Uchwala.__name__])


class UkazForm(forms.ModelForm):
    class Meta:
        model = Ukaz
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets["Ukaz"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["autorzy"].queryset = Byt.objects.instance_of(
            apps.get_model(osoby["Czlonek"]), apps.get_model(osoby["Zarzad"])
        )


class ZrodloForm(forms.ModelForm):
    class Meta:
        model = Zrodlo
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Zrodlo.__name__])


class ZrodloOgolneForm(forms.ModelForm):
    class Meta:
        model = ZrodloOgolne
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[ZrodloOgolne.__name__])
