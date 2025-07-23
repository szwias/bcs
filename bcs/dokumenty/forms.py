from django import forms
from .models import Dokument, Edykt, Ukaz
from osoby.models import Czlonek
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets


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
        self.fields["autorzy"].queryset = Czlonek.objects.all()


class UkazForm(forms.ModelForm):
    class Meta:
        model = Ukaz
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets["Ukaz"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["autorzy"].queryset = Czlonek.objects.all()
