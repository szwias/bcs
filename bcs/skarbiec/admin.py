from core.admin_imports import *
from .model_imports import *
from .inlines import TransakcjaInline


@admin.register(Konto)
class KontoAdmin(BaseModelAdmin):
    list_display = ["get_name", "opis"]
    list_filter_exclude = "__all__"
    inlines = [TransakcjaInline]


@admin.register(Transakcja)
class TransakcjaAdmin(BaseModelAdmin):
    list_display = ["data", "konto", "typ", "get_kwota"]

    def get_kwota(self, obj):
        return obj.get_kwota

    get_kwota.short_description = "Kwota"


register_all_models(
    custom_admins={
        Konto: KontoAdmin,
        Transakcja: TransakcjaAdmin,
    }
)
