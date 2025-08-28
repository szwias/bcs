from nested_admin.nested import NestedStackedInline

from zrodla.inlines import RozliczenieInline
from .models import Transakcja
from .forms import TransakcjaForm


class TransakcjaInline(NestedStackedInline):
    model = Transakcja
    form = TransakcjaForm
    extra = 0
    inlines = [RozliczenieInline]
    show_change_link = True
    ordering = ["data"]
