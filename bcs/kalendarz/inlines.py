from django.contrib import admin

from core.utils.autocompletion.AdvancedInlines import ParentAwareInline
from kalendarz.models import Zdarzenie, ObrazZdarzenie, ObrazWydarzenie
from .forms import ZdarzenieInlineForm


class ObrazWydarzenieInline(admin.StackedInline):
    model = ObrazWydarzenie
    extra = 0
    filter_horizontal = ["widoczne_osoby"]


class ZdarzenieInline(ParentAwareInline, admin.StackedInline):
    model = Zdarzenie
    form = ZdarzenieInlineForm
    extra = 0
    show_change_link = True
    ordering = ["data", "godzina"]
    filter_horizontal = ["powiazane_osoby"]


class ObrazZdarzenieInline(admin.StackedInline):
    model = ObrazZdarzenie
    extra = 0
    fields = ["tytul", "obraz"]
    show_change_link = True