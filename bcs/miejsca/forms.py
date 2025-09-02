from django import forms
from core.forms import create_model_forms
from .model_imports import *
from .views import autocomplete_widgets
from core.autocompletion.registry import build_widgets


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

model_forms = create_model_forms(autocomplete_widgets)

