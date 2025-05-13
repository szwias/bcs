from core.utils.automation.BaseAdmin import *
from .forms import OsobyForm
from .models import *
from django.contrib.contenttypes.admin import GenericTabularInline


class OsobyInline(GenericTabularInline):
    model = Osoby
    extra = 1
    verbose_name = "Osoba"
    verbose_name_plural = "Osoby"
    form = OsobyForm

class ObrazWydarzenieInline(admin.StackedInline):  # or StackedInline
    model = ObrazWydarzenie
    extra = 1
    verbose_name = "Zdjęcie z wydarzenia"
    verbose_name_plural = "Zdjęcia z wydarzeń"

@admin.register(Wyjazd)
class WyjazdAdmin(BaseModelAdmin):
    inlines = [OsobyInline]
    save_as = True

@admin.register(ObrazWydarzenie)
class ObrazWydarzenieAdmin(BaseModelAdmin):
    inlines = [OsobyInline]
    save_as = True

@admin.register(Wydarzenie)
class WydarzenieAdmin(BaseModelAdmin):
    inlines = [OsobyInline, ObrazWydarzenieInline]
    save_as = True
    filter_horizontal = ("zdarzenia", "obrazy",)


@admin.register(Zdarzenie)
class ZdarzenieAdmin(BaseModelAdmin):
    inlines = [OsobyInline]
    save_as = True


register_all_models(
    custom_admins={
        ObrazWydarzenie: ObrazWydarzenieAdmin,
        Wydarzenie: WydarzenieAdmin,
        Wyjazd: WyjazdAdmin,
        Zdarzenie: ZdarzenieAdmin,
    }
)
