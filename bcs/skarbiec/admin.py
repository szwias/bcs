from nested_admin.nested import NestedModelAdmin

from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models
)
from skarbiec.models import (
    Konto,
    Transakcja,
)
from zrodla.inlines import RozliczenieInline
from .inlines import TransakcjaInline


@admin.register(Konto)
class KontoAdmin(NestedModelAdmin, BaseModelAdmin):
    list_display = ["wlasciciel", "opis"]
    inlines = [TransakcjaInline]

@admin.register(Transakcja)
class TransakcjaAdmin(BaseModelAdmin):
    inlines = [RozliczenieInline]


register_all_models(
    custom_admins={
        Konto: KontoAdmin,
        Transakcja: TransakcjaAdmin,
    }
)
