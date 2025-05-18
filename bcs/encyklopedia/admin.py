from core.utils.automation.BaseAdmin import *
from .models import Bractwo, TradycjaBCS


@admin.register(Bractwo)
class BractwoAdmin(BaseModelAdmin):
    list_filter_exclude = ["rok_zalozenia"]

@admin.register(TradycjaBCS)
class TradycjaBCSAdmin(BaseModelAdmin):
    list_filter_exclude = ["wydarzenie"]

register_all_models(
    custom_admins={
        Bractwo: BractwoAdmin,
        TradycjaBCS: TradycjaBCSAdmin,
    }
)
