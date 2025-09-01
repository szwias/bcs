from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models,
)
from .model_imports import *


@admin.register(ObrazWydarzenie)
class ObrazWydarzenieAdmin(BaseModelAdmin):
    save_as = True
    filter_horizontal = ["widoczne_osoby"]


@admin.register(ObrazZdarzenie)
class ObrazZdarzenieAdmin(BaseModelAdmin):
    save_as = True
    filter_horizontal = ["widoczne_osoby"]


register_all_models(
    custom_admins={
        ObrazWydarzenie: ObrazWydarzenieAdmin,
        ObrazZdarzenie: ObrazZdarzenieAdmin,
    }
)
