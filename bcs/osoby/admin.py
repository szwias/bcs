from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models,
)
from core.utils.filters import UsedContentTypeFilter
from .inlines import KoordynatorZespoluInline
from .models import (
    Bean,
    Czlonek,
    DawnyZarzad,
    HallOfFame,
    ImieSzlacheckie,
    InnaOsoba,
    KomisjaRewizyjna,
    NowyZarzad,
    Osoba,
    WielkiMistrz,
    ZwierzeCzapkowe, Zespol,
)
from kronika.inlines import PodsumowanieKadencjiInline


class OsobyUsedContentTypeFilter(UsedContentTypeFilter):
    title = "Typ osoby"
    parameter_name = "typ_osoby"


@admin.register(Osoba)
class OsobaAdmin(BaseModelAdmin):
    list_filter = [OsobyUsedContentTypeFilter]


@admin.register(Bean)
class BeanAdmin(BaseModelAdmin):
    list_filter = ["staz", "pewnosc_stazu"]


@admin.register(Czlonek)
class CzlonekAdmin(BaseModelAdmin):
    list_filter_exclude = ["polymorphic_ctype", "osoba_ptr", "byt_ptr"]


@admin.register(InnaOsoba)
class InnaOsobaAdmin(BaseModelAdmin):
    list_filter_exclude = ["polymorphic_ctype", "osoba_ptr"]


@admin.register(DawnyZarzad)
class DawnyZarzadAdmin(BaseModelAdmin):
    list_filter_exclude = "__all__"
    inlines = [PodsumowanieKadencjiInline]


@admin.register(NowyZarzad)
class ZarzadAdmin(BaseModelAdmin):
    list_filter_exclude = "__all__"
    inlines = [PodsumowanieKadencjiInline]


@admin.register(HallOfFame)
class HallOfFameAdmin(BaseModelAdmin):
    list_filter_exclude = "__all__"


@admin.register(ImieSzlacheckie)
class ImieSzlacheckieAdmin(BaseModelAdmin):
    list_filter_exclude = "__all__"


@admin.register(WielkiMistrz)
class WielkiMistrzAdmin(BaseModelAdmin):
    list_filter_exclude = "__all__"


@admin.register(ZwierzeCzapkowe)
class ZwierzeCzapkoweAdmin(BaseModelAdmin):
    list_filter_exclude = "__all__"


@admin.register(KomisjaRewizyjna)
class KomisjaRewizyjnaAdmin(BaseModelAdmin):
    list_filter_exclude = "__all__"
    filter_horizontal = ["sklad"]


@admin.register(Zespol)
class ZespolAdmin(BaseModelAdmin):
    inlines = [KoordynatorZespoluInline]
    filter_horizontal = ["czlonkowie"]


register_all_models(
    custom_admins={
        Bean: BeanAdmin,
        Czlonek: CzlonekAdmin,
        DawnyZarzad: DawnyZarzadAdmin,
        NowyZarzad: ZarzadAdmin,
        HallOfFame: HallOfFameAdmin,
        ImieSzlacheckie: ImieSzlacheckieAdmin,
        InnaOsoba: InnaOsobaAdmin,
        KomisjaRewizyjna: KomisjaRewizyjnaAdmin,
        Osoba: OsobaAdmin,
        WielkiMistrz: WielkiMistrzAdmin,
        Zespol: ZespolAdmin,
        ZwierzeCzapkowe: ZwierzeCzapkoweAdmin,
    }
)
