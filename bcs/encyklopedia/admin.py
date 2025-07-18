from core.utils.automation.BaseAdmin import *
from .models import Bractwo, TradycjaBCS, GrupaBractw


@admin.register(Bractwo)
class BractwoAdmin(BaseModelAdmin):
    list_filter_exclude = ['rok_zalozenia']

@admin.register(GrupaBractw)
class GrupaBractwAdmin(BaseModelAdmin):
    filter_horizontal = ['kraje']

@admin.register(TradycjaBCS)
class TradycjaBCSAdmin(BaseModelAdmin):
    list_filter_exclude = ['wydarzenie']

register_all_models(
    custom_admins={
        Bractwo: BractwoAdmin,
        GrupaBractw: GrupaBractwAdmin,
        TradycjaBCS: TradycjaBCSAdmin,
    }
)
