from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models,
)
from kronika.models import Kadencja, WydarzenieHistoryczne


@admin.register(Kadencja)
class KadencjaAdmin(BaseModelAdmin):
    list_filter_exclude = "__all__"


@admin.register(WydarzenieHistoryczne)
class WydarzenieHistoryczneAdmin(BaseModelAdmin):
    list_filter = ["typ"]


register_all_models(
    custom_admins={
        Kadencja: KadencjaAdmin,
        WydarzenieHistoryczne: WydarzenieHistoryczneAdmin,
    }
)
