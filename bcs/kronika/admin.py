from core.utils.automation.BaseAdmin import *
from .models import ObrazWydarzenie, ObrazZdarzenie, Wydarzenie, Zdarzenie
from .inlines import ZdarzenieInline, ObrazWydarzenieInline, ObrazZdarzenieInline


@admin.register(ObrazWydarzenie)
class ObrazWydarzenieAdmin(BaseModelAdmin):
    save_as = True
    filter_horizontal = ["widoczne_osoby"]

@admin.register(ObrazZdarzenie)
class ObrazZdarzenieAdmin(BaseModelAdmin):
    save_as = True
    filter_horizontal = ["widoczne_osoby"]

@admin.register(Wydarzenie)
class WydarzenieAdmin(BaseModelAdmin):
    save_as = True
    inlines = [ZdarzenieInline, ObrazWydarzenieInline]
    filter_horizontal = ("miejsca", "uczestnicy")

@admin.register(Zdarzenie)
class ZdarzenieAdmin(BaseModelAdmin):
    inlines = [ObrazZdarzenieInline]
    filter_horizontal = ["powiazane_osoby"]
    save_as = True


register_all_models(
    custom_admins={
        ObrazWydarzenie: ObrazWydarzenieAdmin,
        ObrazZdarzenie: ObrazZdarzenieAdmin,
        Wydarzenie: WydarzenieAdmin,
        Zdarzenie: ZdarzenieAdmin,
    }
)
