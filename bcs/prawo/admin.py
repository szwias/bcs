from core.admin_imports import *
from prawo.inlines import PrawoObowiazekInline
from .models_imports import *


@admin.register(Podmiot)
class PodmiotAdmin(BaseModelAdmin):
    # hide_base_class_from_index = False
    pass


@admin.register(RelacjaPrawna)
class RelacjaPrawnaAdmin(BaseModelAdmin):
    list_filter = ["prawo_czy_obowiazek"]
    list_display = ["tresc", "prawo_czy_obowiazek"]


@admin.register(Rola)
class RolaAdmin(BaseModelAdmin):
    list_display = ["nazwa", "aktualne", "dlugosc_kadencji"]
    inlines = [PrawoObowiazekInline]
    list_filter_exclude = ["polymorphic_ctype", "podmiot_ptr"]


@admin.register(Struktura)
class StrukturaAdmin(RolaAdmin):
    list_display = ["nazwa", "aktualne", "wielkosc", "dlugosc_kadencji"]


@admin.register(PrawoObowiazek)
class PrawoObowiazekAdmin(BaseModelAdmin):
    list_display = ["podmiot", "relacja", "aktualne"]
    list_filter_exclude = ["relacja"]


register_all_models()
