from nested_admin.nested import NestedStackedInline
from core.utils.autocompletion.AdvancedInlines import ParentAwareInline
from kalendarz.models import Zdarzenie
from multimedia.inlines import ObrazZdarzenieInline
from .forms import ZdarzenieInlineForm


class ZdarzenieInline(NestedStackedInline, ParentAwareInline):
    model = Zdarzenie
    form = ZdarzenieInlineForm
    inlines = [ObrazZdarzenieInline]
    extra = 1
    show_change_link = True
    ordering = ["data", "godzina"]
    filter_horizontal = ["powiazane_osoby"]
