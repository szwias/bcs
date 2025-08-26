from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models,
)
from .models import Dokument, Edykt, Ukaz, Zrodlo, ZrodloOgolne


@admin.register(Zrodlo)
class ZrodloAdmin(BaseModelAdmin):
    filter_horizontal = ["autorzy"]


@admin.register(Dokument)
class DokumentAdmin(ZrodloAdmin):
    list_filter_exclude = ["polymorphic_ctype"]
    list_display = ["tytul", "streszczenie"]


@admin.register(ZrodloOgolne)
class ZrodloOgolneAdmin(ZrodloAdmin):
    list_filter_exclude = ["zrodlo_ptr"]


@admin.register(Edykt)
class EdyktAdmin(DokumentAdmin):
    fields = ["tytul", "numer", "data", "autorzy", "streszczenie", "plik"]
    list_filter_exclude = ["dokument_ptr", "polymorphic_ctype", "zrodlo_ptr"]


@admin.register(Ukaz)
class UkazAdmin(DokumentAdmin):
    fields = ["tytul", "numer", "data", "autorzy", "streszczenie", "plik"]
    list_filter_exclude = ["dokument_ptr", "polymorphic_ctype", "zrodlo_ptr"]


register_all_models(
    custom_admins={
        Dokument: DokumentAdmin,
        Edykt: EdyktAdmin,
        Ukaz: UkazAdmin,
        Zrodlo: ZrodloAdmin,
        ZrodloOgolne: ZrodloAdmin,
    }
)
