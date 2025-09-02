from core.admin_imports import *
from .model_imports import *


@admin.register(Zrodlo)
class ZrodloAdmin(BaseModelAdmin):
    filter_horizontal = ["autorzy"]


@admin.register(Dokument)
class DokumentAdmin(ZrodloAdmin):
    list_filter_exclude = ["polymorphic_ctype"]
    list_display = ["tytul", "streszczenie"]


@admin.register(Rozliczenie)
class RozliczenieAdmin(DokumentAdmin):
    pass


@admin.register(ZrodloOgolne)
class ZrodloOgolneAdmin(ZrodloAdmin):
    list_filter_exclude = ["zrodlo_ptr"]


@admin.register(Oswiadczenie)
class OswiadczenieAdmin(DokumentAdmin):
    fields = ["tytul", "data", "autorzy", "streszczenie", "plik"]
    list_filter_exclude = ["dokument_ptr", "polymorphic_ctype", "zrodlo_ptr"]
    list_display = ["tytul", "get_autor", "streszczenie"]

    def get_autor(self, obj):
        return obj.get_autor

    get_autor.short_description = "Autorzy"


@admin.register(Uchwala)
class UchwalaAdmin(OswiadczenieAdmin):
    fields = ["tytul", "data", "walne", "autorzy", "streszczenie", "plik"]
    list_filter_exclude = "__all__"
    list_display = ["tytul", "data", "get_autor", "streszczenie"]


@admin.register(Korespondencja)
class KorespondencjaAdmin(BaseModelAdmin):
    fields = ["tytul", "data", "autorzy", "adresaci", "streszczenie", "plik"]
    list_filter_exclude = ["dokument_ptr", "polymorphic_ctype", "zrodlo_ptr"]
    filter_horizontal = ["autorzy", "adresaci"]
    list_display = ["tytul", "data", "streszczenie"]


@admin.register(Ukaz)
class UkazAdmin(DokumentAdmin):
    fields = ["tytul", "numer", "data", "autorzy", "streszczenie", "plik"]
    list_filter_exclude = ["dokument_ptr", "polymorphic_ctype", "zrodlo_ptr"]


@admin.register(Edykt)
class EdyktAdmin(UkazAdmin):
    pass


register_all_models()
