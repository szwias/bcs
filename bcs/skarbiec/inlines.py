from django.contrib.admin import StackedInline

from .models import Transakcja
from .forms import TransakcjaForm


class TransakcjaInline(StackedInline):
    model = Transakcja
    form = TransakcjaForm
    extra = 0
    show_change_link = True
    ordering = ["data"]
