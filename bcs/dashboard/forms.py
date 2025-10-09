from dal import autocomplete

from django import forms

from core.autocompletion.registry import build_widgets
from core.forms import create_model_forms
from .autocomplete_views import autocomplete_widgets
from .models import App


class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = "__all__"
        widgets = build_widgets(autocomplete_widgets[App.__name__])
        widgets.update(
            {
                "adres_url": autocomplete.ListSelect2(
                    url="dashboard_autocomplete:"
                    "custom-app-django-url-autocomplete",
                    forward=["aplikacja"],
                )
            }
        )


model_forms = create_model_forms(autocomplete_widgets)
