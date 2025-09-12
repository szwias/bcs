from django.contrib.admin import StackedInline

from .forms import model_forms
from .models import Transakcja


class TransakcjaInline(StackedInline):
    model = Transakcja
    form = model_forms["TransakcjaForm"]
    extra = 0
    show_change_link = True
    ordering = ["data"]
