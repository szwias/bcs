from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models,
)
from .model_imports import *


@admin.register(Piosenka)
class PiosenkaAdmin(BaseModelAdmin):
    filter_horizontal = ["kategorie", "znani_czapce_autorzy"]
    list_filter = ["kategorie", "znani_czapce_autorzy"]


register_all_models(custom_admins={Piosenka: PiosenkaAdmin})
