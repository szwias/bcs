from core.admin import BaseModelAdmin1
from core.admin_imports import *
from .model_imports import *


@admin.register(Aforyzm)
class AforyzmAdmin(BaseModelAdmin1):
    filter_horizontal = ["adresaci"]


@admin.register(Cytat)
class CytatAdmin(BaseModelAdmin1):
    filter_horizontal = ["adresaci"]


@admin.register(GrupaBractw)
class GrupaBractwAdmin(BaseModelAdmin1):
    filter_horizontal = ["kraje"]
    list_display = ["nazwa", "panstwa"]

    def panstwa(self, obj):
        return obj.get_kraje

    panstwa.short_description = "Państwa"


@admin.register(Powiedzenie)
class PowiedzenieAdmin(BaseModelAdmin1):
    filter_horizontal = ["adresaci"]


@admin.register(TradycjaBCS)
class TradycjaBCSAdmin(BaseModelAdmin1):
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
