from django.contrib.postgres.aggregates import StringAgg

from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models,
)
from prawo.models import RelacjaPrawna


@admin.register(RelacjaPrawna)
class RelacjaPrawnaAdmin(BaseModelAdmin):
    filter_horizontal = ["podmiot"]
    list_filter = ["prawo_czy_obowiazek", "podmiot", "przedawnione"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            podmiot_list=StringAgg("podmiot__nazwa", delimiter=", ")
        ).order_by("podmiot_list")


register_all_models(
    custom_admins={
        RelacjaPrawna: RelacjaPrawnaAdmin,
    }
)
