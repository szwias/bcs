from core.utils.automation.BaseAdmin import *
from .models import Dokument, Edykt, Ukaz


@admin.register(Dokument)
class DokumentAdmin(BaseModelAdmin):
    filter_horizontal = ["autorzy"]
    list_filter_exclude = ["polymorphic_ctype"]


@admin.register(Edykt)
class EdyktAdmin(BaseModelAdmin):
    fields = ["tytul", "numer", "data", "autorzy", "streszczenie", "plik"]
    filter_horizontal = ["autorzy"]
    list_filter_exclude = ["polymorphic_ctype"]


@admin.register(Ukaz)
class UkazAdmin(BaseModelAdmin):
    fields = ["tytul", "numer", "data", "autorzy", "streszczenie", "plik"]
    filter_horizontal = ["autorzy"]
    list_filter_exclude = ["polymorphic_ctype"]


register_all_models(
    custom_admins={
        Dokument: DokumentAdmin,
        Edykt: EdyktAdmin,
        Ukaz: UkazAdmin,
    }
)
