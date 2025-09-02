from core.admin_imports import *
from .model_imports import *


@admin.register(Piosenka)
class PiosenkaAdmin(BaseModelAdmin):
    filter_horizontal = ["kategorie", "znani_czapce_autorzy"]
    list_filter = ["kategorie", "znani_czapce_autorzy"]


register_all_models()
