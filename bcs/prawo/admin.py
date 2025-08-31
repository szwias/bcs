from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models,
)
from prawo.inlines import PrawoObowiazekInline
from prawo.models import (
    PrawoObowiazek,
    RelacjaPrawna,
    Rola,
    Struktura,
)


@admin.register(RelacjaPrawna)
class RelacjaPrawnaAdmin(BaseModelAdmin):
    list_filter = ["prawo_czy_obowiazek"]
    list_display = ["tresc", "prawo_czy_obowiazek"]


@admin.register(Rola)
class RolaAdmin(BaseModelAdmin):
    list_display = ["nazwa", "aktualne"]
    inlines = [PrawoObowiazekInline]


@admin.register(Struktura)
class StrukturaAdmin(RolaAdmin):
    pass


@admin.register(PrawoObowiazek)
class PrawoObowiazekAdmin(BaseModelAdmin):
    list_display = ["podmiot", "relacja", "aktualne"]
    list_filter_exclude = ["relacja"]


register_all_models(
    custom_admins={
        PrawoObowiazek: PrawoObowiazekAdmin,
        Rola: RolaAdmin,
        Struktura: StrukturaAdmin,
        RelacjaPrawna: RelacjaPrawnaAdmin,
    }
)
