from django.contrib import admin

from .models import ObrazZdarzenie, ObrazWydarzenie, Zdarzenie
from .forms import ZdarzenieInlineForm

class ObrazWydarzenieInline(admin.StackedInline):  # or StackedInline
    model = ObrazWydarzenie
    extra = 0

class ZdarzenieInline(admin.StackedInline):
    model = Zdarzenie
    form = ZdarzenieInlineForm
    extra = 0
    show_change_link = True
    ordering = ["data", "godzina"]

class ObrazZdarzenieInline(admin.StackedInline):
    model = ObrazZdarzenie
    extra = 0
    fields = ["tytul", "obraz"]
    show_change_link = True