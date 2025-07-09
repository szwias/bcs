"""
from django import drzewo
from dal import autocomplete
from .models import *
from .views import autocomplete_widgets, build_widgets

class ZarzadForm(drzewo.ModelForm):
    class Meta:
        model = Zarzad
        fields = '__all__'

        widgets = build_widgets(autocomplete_widgets['DawnyZarzad'])
        widgets.update({'kadencja': autocomplete.ModelSelect2(url='core:custom-kadencja-autocomplete')})
"""
