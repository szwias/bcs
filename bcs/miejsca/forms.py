from django import forms

from core.autocompletion.registry import build_widgets
from core.forms import create_model_forms
from .autocomplete_views import autocomplete_widgets
from .model_imports import *


class MiejsceForm(forms.ModelForm):
    coordinates = forms.CharField(
        required=False,
        disabled=False,
        label="Współrzędne geograficzne - podaj jeśli w górach (prawy przycisk myszy na czerwony znacznik w Google Maps)",
        widget=forms.TextInput(
            attrs={
                "placeholder": "49.41898, 19.09752",
                "size": 40,
                "rows": 1,
            }
        ),
    )

    class Meta:
        model = Miejsce
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[Miejsce.__name__])
        widgets.update(
            {
                "adres": forms.Textarea(
                    attrs={
                        "placeholder": "<Ulica>, <Kod pocztowy> <Miasto>, <Kraj>",
                        "rows": 1,
                        "cols": 50,
                    }
                ),
                "coordinates": forms.TextInput(
                    attrs={
                        "rows": 1,
                        "cols": 50,
                    }
                ),
            },
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (
            self.instance
            and self.instance.latitude
            and self.instance.longitude
        ):
            self.fields["coordinates"].initial = (
                f"{self.instance.latitude}, {self.instance.longitude}"
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        coords = self.cleaned_data.get("coordinates")
        if coords and (
            instance.latitude is None or instance.longitude is None
        ):
            try:
                lat_str, lon_str = [c.strip() for c in coords.split(",")]
                instance.latitude = float(lat_str)
                instance.longitude = float(lon_str)
            except ValueError:
                raise forms.ValidationError(
                    "Nieprawidłowy format współrzędnych. Użyj 'lat, lon'."
                )

        if commit:
            instance.save()
        return instance


model_forms = create_model_forms(autocomplete_widgets)
