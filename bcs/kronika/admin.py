from core.utils.automation.BaseAdmin import *
from .models import ObrazWydarzenie, Wydarzenie, Zdarzenie
from .inlines import ZdarzenieInline, ObrazWydarzenieInline, ObrazZdarzenieInline


@admin.register(ObrazWydarzenie)
class ObrazWydarzenieAdmin(BaseModelAdmin):
    save_as = True

@admin.register(Wydarzenie)
class WydarzenieAdmin(BaseModelAdmin):
    inlines = [ZdarzenieInline, ObrazWydarzenieInline]
    save_as = True
    filter_horizontal = ("obrazy", "miejsca")

@admin.register(Zdarzenie)
class ZdarzenieAdmin(BaseModelAdmin):
    inlines = [ObrazZdarzenieInline]
    save_as = True


register_all_models(
    custom_admins={
        ObrazWydarzenie: ObrazWydarzenieAdmin,
        Wydarzenie: WydarzenieAdmin,
        Zdarzenie: ZdarzenieAdmin,
    }
)
