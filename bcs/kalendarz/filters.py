from django.contrib import admin

from core.utils.Czas import ROK_ZALOZENIA, BIEZACY_ROK


class YearListFilter(admin.SimpleListFilter):
    title = "Rok"
    parameter_name = "rok"

    def lookups(self, request, model_admin):
        years = range(ROK_ZALOZENIA, BIEZACY_ROK + 1)
        return [(year, year) for year in years]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(data_rozpoczecia__year=self.value())
        return queryset
