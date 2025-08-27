from django import forms
from django.apps import apps

from .models import Dokument, Edykt, Ukaz, Zrodlo, ZrodloOgolne
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets
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
        self.fields['autorzy'].queryset = Byt.objects.instance_of(
            apps.get_model(osoby["Czlonek"]), apps.get_model(osoby["Zarzad"])
        )


class UkazForm(forms.ModelForm):
    class Meta:
        model = Ukaz
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets["Ukaz"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['autorzy'].queryset = Byt.objects.instance_of(
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
