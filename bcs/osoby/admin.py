from core.admin_imports import *
from core.utils.Filters import UsedContentTypeFilter
from kronika.inlines import PodsumowanieKadencjiInline
from .inlines import KoordynatorZespoluInline, EgzekutorInline
from .model_imports import *


class OsobyUsedContentTypeFilter(UsedContentTypeFilter):
    title = "Typ osoby"
    parameter_name = "typ_osoby"


class OrganizacjeUsedContentTypeFilter(UsedContentTypeFilter):
    title = "Typ organizacji"
    parameter_name = "typ_organizacji"


@admin.register(Byt)
class BytAdmin(BaseModelAdmin):
    # hide_base_class_from_index = False
    pass


@admin.register(Osoba)
class OsobaAdmin(BaseModelAdmin):
    list_filter = [OsobyUsedContentTypeFilter]
    # hide_base_class_from_index = False


@admin.register(Bean)
class BeanAdmin(BaseModelAdmin):
    list_filter = ["staz", "pewnosc_stazu"]


@admin.register(Czlonek)
class CzlonekAdmin(BaseModelAdmin):
    list_filter_exclude = ["polymorphic_ctype", "osoba_ptr", "byt_ptr"]


@admin.register(InnaOsoba)
class InnaOsobaAdmin(CzlonekAdmin):
    pass


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
    inlines = [KoordynatorZespoluInline, EgzekutorInline]
    filter_horizontal = ["czlonkowie"]


@admin.register(KoordynatorZespolu)
class KoordynatorZespoluAdmin(BaseModelAdmin):
    list_display = ["zespol", "osoba"]


@admin.register(Organizacja)
class OrganizacjaAdmin(BaseModelAdmin):
    filter_horizontal = ["zalozyciele"]
    list_filter = [OrganizacjeUsedContentTypeFilter]
    hide_base_class_from_index = False


@admin.register(OrganizacjaStudencka)
class OrganizacjaStudenckaAdmin(BaseModelAdmin):
    list_filter = ["kraj", "uczelnia"]
    filter_horizontal = ["zalozyciele"]
    hide_base_class_from_index = False


@admin.register(Bractwo)
class BractwoAdmin(OrganizacjaStudenckaAdmin):
    list_filter = ["grupa_bractw", "kraj"]


register_all_models()
