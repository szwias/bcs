from django import forms
from dal import autocomplete
from .models import *
from .views import autocomplete_widgets
from core.utils.autocompletion.AutocompletesGeneration import build_widgets
