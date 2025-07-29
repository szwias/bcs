from django.contrib import admin
from .models import ObrazWydarzenie, ObrazZdarzenie


class ObrazInline(admin.StackedInline):
    extra = 0
    fields = ["tytul", "obraz"]
    show_change_link = True


class ObrazWydarzenieInline(ObrazInline):
    model = ObrazWydarzenie
    filter_horizontal = ["widoczne_osoby"]


class ObrazZdarzenieInline(ObrazInline):
    model = ObrazZdarzenie
    filter_horizontal = ["widoczne_osoby"]
