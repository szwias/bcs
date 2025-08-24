from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models
)
from .models import Piosenka

@admin.register(Piosenka)
class PiosenkaAdmin(BaseModelAdmin):
    filter_horizontal = ["kategorie", "znani_czapce_autorzy"]
    list_filter = ["kategorie"]

register_all_models(
    custom_admins={
        Piosenka: PiosenkaAdmin
    }
)
