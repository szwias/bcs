from core.admin_imports import *
from .model_imports import *


@admin.register(Zwrot)
class ZwrotAdmin(BaseModelAdmin):
    list_display = ["zwrot", "tlumaczenie", "uzywany_na_karczmie"]


register_all_models()
