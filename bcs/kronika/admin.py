from core.utils.automation.BaseAdmin import *
from czlonkowie.forms import OsobyForm
from czlonkowie.models import Osoby
from .forms import ZdarzenieInlineForm
from .models import *
from django.contrib.contenttypes.admin import GenericTabularInline


class OsobyInline(GenericTabularInline):
    model = Osoby
    extra = 0
    form = OsobyForm

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

@admin.register(ObrazWydarzenie)
class ObrazWydarzenieAdmin(BaseModelAdmin):
    inlines = [OsobyInline]
    save_as = True

@admin.register(Wydarzenie)
class WydarzenieAdmin(BaseModelAdmin):
    inlines = [ZdarzenieInline, OsobyInline, ObrazWydarzenieInline]
    save_as = True
    filter_horizontal = ("obrazy", "miejsca")


@admin.register(Zdarzenie)
class ZdarzenieAdmin(BaseModelAdmin):
    inlines = [OsobyInline, ObrazZdarzenieInline]
    save_as = True



register_all_models(
    custom_admins={
        ObrazWydarzenie: ObrazWydarzenieAdmin,
        Wydarzenie: WydarzenieAdmin,
        Zdarzenie: ZdarzenieAdmin,
    }
)
