from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models
)
from skarbiec.models import (
    Konto,
)
from .inlines import TransakcjaInline


@admin.register(Konto)
class KontoAdmin(BaseModelAdmin):
    list_display = ["wlasciciel", "opis"]
    inlines = [TransakcjaInline]


register_all_models(
    custom_admins={
        Konto: KontoAdmin,
    }
)
