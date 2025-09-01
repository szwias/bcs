from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models,
)
from .model_imports import *


@admin.register(Zwrot)
class ZwrotAdmin(BaseModelAdmin):
    list_display = ["zwrot", "tlumaczenie", "uzywany_na_karczmie"]


register_all_models(
    custom_admins={
        Zwrot: ZwrotAdmin,
    }
)
