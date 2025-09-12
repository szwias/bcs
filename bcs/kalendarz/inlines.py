from nested_admin.nested import NestedStackedInline

from core.inlines import ParentAwareInline
from multimedia.inlines import ObrazZdarzenieInline
from .forms import ZdarzenieInlineForm
from .models import Zdarzenie


class ZdarzenieInline(NestedStackedInline, ParentAwareInline):
    model = Zdarzenie
    form = ZdarzenieInlineForm
    inlines = [ObrazZdarzenieInline]
    extra = 0
    show_change_link = True
    ordering = ["data", "godzina"]
    filter_horizontal = ["powiazane_osoby"]
