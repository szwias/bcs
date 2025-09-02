from django.contrib.admin import StackedInline

from .models import Transakcja
from .forms import model_forms


class TransakcjaInline(StackedInline):
    model = Transakcja
    form = model_forms["TransakcjaForm"]
    extra = 0
    show_change_link = True
    ordering = ["data"]
