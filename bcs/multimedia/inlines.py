from nested_admin.nested import NestedStackedInline
from .models import ObrazWydarzenie, ObrazZdarzenie


class ObrazInline(NestedStackedInline):
    extra = 0
    fields = ["tytul", "obraz"]
    show_change_link = True


class ObrazWydarzenieInline(ObrazInline):
    model = ObrazWydarzenie
    filter_horizontal = ["widoczne_osoby"]


class ObrazZdarzenieInline(ObrazInline):
    model = ObrazZdarzenie
    filter_horizontal = ["widoczne_osoby"]
    extra = 0  # ensures a form is available for new ZdarzenieInline
