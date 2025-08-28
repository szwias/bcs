from nested_admin.nested import NestedStackedInline

from zrodla.forms import RozliczenieForm
from zrodla.models import Rozliczenie


class RozliczenieInline(NestedStackedInline):
    model = Rozliczenie
    form = RozliczenieForm
    extra = 1
    ordering = ["tytul"]
    filter_horizontal = ["autorzy"]
