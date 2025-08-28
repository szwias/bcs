from django.contrib.postgres.aggregates import StringAgg
from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models,
)
from prawo.models import (
    RelacjaPrawna,
    Rola,
)


@admin.register(RelacjaPrawna)
class RelacjaPrawnaAdmin(BaseModelAdmin):
    filter_horizontal = ["podmiot"]
    list_filter = ["prawo_czy_obowiazek", "podmiot", "aktualne"]
    list_display = [
        "get_podmiot",
        "prawo_czy_obowiazek",
        "tresc",
        "aktualne"
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            podmiot_list=StringAgg("podmiot__nazwa", delimiter=", ")
        ).order_by("podmiot_list")

    def get_podmiot(self, obj):
        return ", ".join([str(p) for p in obj.podmiot.all()])
    get_podmiot.short_description = "Podmiot"


@admin.register(Rola)
class RolaAdmin(BaseModelAdmin):
    list_display = ["nazwa", "aktualne"]


register_all_models(
    custom_admins={
        Rola: RolaAdmin,
        RelacjaPrawna: RelacjaPrawnaAdmin,
    }
)
