from kalendarz.filters import YearListFilter


class YearFilter(YearListFilter):

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                wydarzenie__data_rozpoczecia__year=self.value()
            )
        return queryset