from core.utils.automation.BaseAdmin import *
from .forms import UczestnictwoForm
from .models import *
from django.contrib.contenttypes.admin import GenericTabularInline


class UczestnictwoInline(GenericTabularInline):
    model = Uczestnictwo
    extra = 1
    verbose_name = "Uczestnictwo"
    verbose_name_plural = "Uczestnictwo"
    form = UczestnictwoForm

class ObrazWydarzenieInline(admin.TabularInline):  # or StackedInline
    model = ObrazWydarzenie
    extra = 1
    verbose_name = "Zdjęcie z wydarzenia"
    verbose_name_plural = "Zdjęcia z wydarzeń"

@admin.register(Wyjazd)
class WyjazdAdmin(BaseModelAdmin):
    inlines = [UczestnictwoInline]
    save_as = True


@admin.register(Wydarzenie)
class WydarzenieAdmin(BaseModelAdmin):
    inlines = [UczestnictwoInline, ObrazWydarzenieInline]
    save_as = True
    filter_horizontal = ("zdarzenia",)


@admin.register(Zdarzenie)
class ZdarzenieAdmin(BaseModelAdmin):
    inlines = [UczestnictwoInline]
    save_as = True


register_all_models(
    custom_admins={
        Wydarzenie: WydarzenieAdmin,
        Wyjazd: WyjazdAdmin,
        Zdarzenie: ZdarzenieAdmin,
    }
)
