from core.utils.automation.BaseAdmin import *
from prawo.models import RelacjaPrawna


@admin.register(RelacjaPrawna)
class RelacjaPrawnaAdmin(BaseModelAdmin):
    filter_horizontal = ["podmiot"]


register_all_models(
    custom_admins={
        RelacjaPrawna: RelacjaPrawnaAdmin,
    }
)
