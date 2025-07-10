from core.utils.automation.BaseAdmin import *
from .models import ObrazWydarzenie, Wydarzenie, Zdarzenie
from .inlines import ZdarzenieInline, ObrazWydarzenieInline, ObrazZdarzenieInline
from czlonkowie.inlines import OsobyInline


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
