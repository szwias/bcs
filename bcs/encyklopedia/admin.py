from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models,
)
from osoby.inlines import InnaOsobaInline
from .models import (
    Aforyzm,
    Bractwo,
    Cytat,
    GrupaBractw,
    Powiedzenie,
    TradycjaBCS,
)


@admin.register(Aforyzm)
class AforyzmAdmin(BaseModelAdmin):
    filter_horizontal = ["adresaci"]


@admin.register(Bractwo)
class BractwoAdmin(BaseModelAdmin):
    list_filter_exclude = ["rok_zalozenia"]
    filter_horizontal = ["zalozyciele"]
    inlines = [InnaOsobaInline]


@admin.register(Cytat)
class CytatAdmin(BaseModelAdmin):
    filter_horizontal = ["adresaci"]


@admin.register(GrupaBractw)
class GrupaBractwAdmin(BaseModelAdmin):
    filter_horizontal = ["kraje"]


@admin.register(Powiedzenie)
class PowiedzenieAdmin(BaseModelAdmin):
    filter_horizontal = ["adresaci"]


@admin.register(TradycjaBCS)
class TradycjaBCSAdmin(BaseModelAdmin):
    list_filter_exclude = ["wydarzenie"]


register_all_models(
    custom_admins={
        Aforyzm: AforyzmAdmin,
        Bractwo: BractwoAdmin,
        Cytat: CytatAdmin,
        GrupaBractw: GrupaBractwAdmin,
        Powiedzenie: PowiedzenieAdmin,
        TradycjaBCS: TradycjaBCSAdmin,
    }
)
