from django import forms
from .model_imports import *
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets


class KrajForm(forms.ModelForm):
    class Meta:
        model = Kraj
        fields = "__all__"

        # widgets = build_widgets(autocomplete_widgets['Kraj'])


class MiejsceForm(forms.ModelForm):
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
                )
            }
        )


class UczelniaForm(forms.ModelForm):
    class Meta:
        model = Uczelnia
        fields = "__all__"

        widgets = build_widgets(autocomplete_widgets["Uczelnia"])


class WydzialForm(forms.ModelForm):
    class Meta:
        model = Wydzial
        fields = "__all__"

        widgets = build_widgets(autocomplete_widgets["Wydzial"])
