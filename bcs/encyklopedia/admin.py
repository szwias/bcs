from core.utils.automation.BaseAdmin import *
from .models import Bractwo, TradycjaBCS, GrupaBractw, Powiedzenie, Zrodlo


@admin.register(Bractwo)
class BractwoAdmin(BaseModelAdmin):
    list_filter_exclude = ['rok_zalozenia']
    filter_horizontal = ['zalozyciele']

@admin.register(GrupaBractw)
class GrupaBractwAdmin(BaseModelAdmin):
    filter_horizontal = ['kraje']

@admin.register(Powiedzenie)
class PowiedzenieAdmin(BaseModelAdmin):
    filter_horizontal = ['adresaci']

@admin.register(TradycjaBCS)
class TradycjaBCSAdmin(BaseModelAdmin):
    list_filter_exclude = ['wydarzenie']

@admin.register(Zrodlo)
class ZrodloAdmin(BaseModelAdmin):
    filter_horizontal = ['autorzy']


register_all_models(
    custom_admins={
        Bractwo: BractwoAdmin,
        GrupaBractw: GrupaBractwAdmin,
        Powiedzenie: PowiedzenieAdmin,
        TradycjaBCS: TradycjaBCSAdmin,
        Zrodlo: ZrodloAdmin
    }
)
