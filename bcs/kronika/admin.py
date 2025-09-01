from django.db.models import Min

from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models,
)
from .model_imports import *
from .filters import YearFilter


@admin.register(Kadencja)
class KadencjaAdmin(BaseModelAdmin):
    list_filter_exclude = "__all__"


@admin.register(WydarzenieHistoryczne)
class WydarzenieHistoryczneAdmin(BaseModelAdmin):
    list_filter = [YearFilter, "typy"]
    filter_horizontal = ["typy"]
    list_display = ["get_data", "get_typ", "nazwa"]

    def get_data(self, obj):
        return obj.get_data

    get_data.short_description = "Data"

    def get_typ(self, obj):
        return ", ".join([str(t) for t in obj.typy.all()])

    get_typ.short_description = "Typ wydarzenia"


@admin.register(ZadanieChrzcielne)
class ZadanieChrzcielneAdmin(BaseModelAdmin):
    filter_horizontal = ["autorzy"]
    list_display = ["get_authors", "nazwa", "kategoria"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            first_author_date=Min(
                "autorzy__chrzest__data_rozpoczecia"
            )
        )

    def first_author_date(self, obj):
        return obj.first_author_date

    first_author_date.admin_order_field = "first_author_date"

    def get_authors(self, obj):
        return ", ".join([str(a) for a in obj.autorzy.all()])

    get_authors.short_description = "Autorzy"


register_all_models(
    custom_admins={
        Kadencja: KadencjaAdmin,
        WydarzenieHistoryczne: WydarzenieHistoryczneAdmin,
        ZadanieChrzcielne: ZadanieChrzcielneAdmin,
    }
)
