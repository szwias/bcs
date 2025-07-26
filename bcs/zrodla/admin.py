from core.utils.automation.BaseAdmin import *
from .models import Dokument, Edykt, Ukaz, Zrodlo, ZrodloOgolne


@admin.register(Zrodlo)
class ZrodloAdmin(BaseModelAdmin):
    filter_horizontal = ["autorzy"]


@admin.register(Dokument)
class DokumentAdmin(ZrodloAdmin):
    list_filter_exclude = ["polymorphic_ctype"]


@admin.register(ZrodloOgolne)
class ZrodloOgolneAdmin(ZrodloAdmin):
    pass


@admin.register(Edykt)
class EdyktAdmin(DokumentAdmin):
    fields = ["tytul", "numer", "data", "autorzy", "streszczenie", "plik"]


@admin.register(Ukaz)
class UkazAdmin(DokumentAdmin):
    fields = ["tytul", "numer", "data", "autorzy", "streszczenie", "plik"]


register_all_models(
    custom_admins={
        Dokument: DokumentAdmin,
        Edykt: EdyktAdmin,
        Ukaz: UkazAdmin,
        Zrodlo: ZrodloAdmin,
        ZrodloOgolne: ZrodloAdmin,
    }
)
