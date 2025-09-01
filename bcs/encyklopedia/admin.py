from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models,
)
from .model_imports import *


@admin.register(Aforyzm)
class AforyzmAdmin(BaseModelAdmin):
    filter_horizontal = ["adresaci"]


@admin.register(Cytat)
class CytatAdmin(BaseModelAdmin):
    filter_horizontal = ["adresaci"]


@admin.register(GrupaBractw)
class GrupaBractwAdmin(BaseModelAdmin):
    filter_horizontal = ["kraje"]
    list_display = ["nazwa", "panstwa"]

    def panstwa(self, obj):
        return obj.get_kraje
    panstwa.short_description = "Państwa"


@admin.register(Powiedzenie)
class PowiedzenieAdmin(BaseModelAdmin):
    filter_horizontal = ["adresaci"]


@admin.register(TradycjaBCS)
class TradycjaBCSAdmin(BaseModelAdmin):
    list_filter_exclude = ["wydarzenie"]


register_all_models(
    custom_admins={
        Aforyzm: AforyzmAdmin,
        Cytat: CytatAdmin,
        GrupaBractw: GrupaBractwAdmin,
        Powiedzenie: PowiedzenieAdmin,
        TradycjaBCS: TradycjaBCSAdmin,
    }
)
