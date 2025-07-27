from core.utils.automation.BaseAdmin import admin, BaseModelAdmin, register_all_models
from prawo.models import RelacjaPrawna


@admin.register(RelacjaPrawna)
class RelacjaPrawnaAdmin(BaseModelAdmin):
    filter_horizontal = ["podmiot"]
    list_filter = ["prawo_czy_obowiazek", "podmiot", "przedawnione"]


register_all_models(
    custom_admins={
        RelacjaPrawna: RelacjaPrawnaAdmin,
    }
)
