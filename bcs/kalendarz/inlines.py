from django.contrib import admin

from core.utils.autocompletion.AdvancedInlines import ParentAwareInline
from kalendarz.models import Zdarzenie
from .forms import ZdarzenieInlineForm


class ZdarzenieInline(ParentAwareInline, admin.StackedInline):
    model = Zdarzenie
    form = ZdarzenieInlineForm
    extra = 0
    show_change_link = True
    ordering = ["data", "godzina"]
    filter_horizontal = ["powiazane_osoby"]
