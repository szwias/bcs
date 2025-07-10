from core.utils.automation.BaseAdmin import *
from .models import Bractwo, TradycjaBCS, Zwyczaj
from czlonkowie.inlines import OsobyInline

class AutorZwyczajuInline(OsobyInline):
    verbose_name = "Autor"
    verbose_name_plural = "Autorzy"

@admin.register(Bractwo)
class BractwoAdmin(BaseModelAdmin):
    list_filter_exclude = ["rok_zalozenia"]

@admin.register(TradycjaBCS)
class TradycjaBCSAdmin(BaseModelAdmin):
    list_filter_exclude = ["wydarzenie"]

@admin.register(Zwyczaj)
class ZwyczajAdmin(BaseModelAdmin):
    inlines = [AutorZwyczajuInline]

register_all_models(
    custom_admins={
        Bractwo: BractwoAdmin,
        TradycjaBCS: TradycjaBCSAdmin,
        Zwyczaj: ZwyczajAdmin,
    }
)
