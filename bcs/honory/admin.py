from core.admin_imports import *
from .model_imports import *


@admin.register(Nagrodzeni)
class NagrodzeniAdmin(BaseModelAdmin):
    list_display = ["osoba", "odznaczenie", "zaslugi"]


@admin.register(Odznaczenie)
class OdznaczenieAdmin(BaseModelAdmin):
    filter_horizontal = ["fundatorzy"]
    list_display = ["nazwa", "opis"]
    list_filter_exclude = "__all__"


register_all_models(
    custom_admins={
        Nagrodzeni: NagrodzeniAdmin,
        Odznaczenie: OdznaczenieAdmin,
    }
)
