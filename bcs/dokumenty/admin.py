from core.utils.automation.BaseAdmin import *
from .models import Dokument, Edykt, Ukaz


@admin.register(Dokument)
class DokumentAdmin(BaseModelAdmin):
    filter_horizontal = ["autorzy"]

@admin.register(Edykt)
class EdyktAdmin(BaseModelAdmin):
    fields = ["tytul", "numer", "autorzy", "tekst"]
    filter_horizontal = ["autorzy"]

@admin.register(Ukaz)
class UkazAdmin(BaseModelAdmin):
    fields = ["tytul", "numer", "autorzy", "tekst"]
    filter_horizontal = ["autorzy"]


register_all_models(
    custom_admins={
        Dokument: DokumentAdmin,
        Edykt: EdyktAdmin,
        Ukaz: UkazAdmin,
    }
)
