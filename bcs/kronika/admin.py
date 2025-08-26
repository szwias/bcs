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
    list_display = [
        "get_data",
        "get_typ",
        "nazwa"
    ]

    def get_data(self, obj):
        return obj.get_data
    get_data.short_description = "Data"

    def get_typ(self, obj):
        return obj.typ
    get_typ.short_description = "Typ wydarzenia"


register_all_models(
    custom_admins={
        Kadencja: KadencjaAdmin,
        WydarzenieHistoryczne: WydarzenieHistoryczneAdmin,
    }
)
