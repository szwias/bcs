from core.utils.automation.BaseAdmin import *
from .models import RodzajCzapki, Czapka

from django.contrib import admin
from django.apps import apps

class UczelniaFilter(admin.SimpleListFilter):
    title = 'Uczelnia'
    parameter_name = 'uczelnia'

    def lookups(self, request, model_admin):
        # Dynamically get the model
        Uczelnia = apps.get_model('miejsca', 'Uczelnia')
        # Get distinct uczelnie used in related Czapka entries
        return [
            (u.id, str(u))
            for u in Uczelnia.objects.filter(wydzial__czapka__isnull=False).distinct()
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(wydzial__uczelnia__id=self.value())
        return queryset

@admin.register(Czapka)
class CzapkaAdmin(BaseModelAdmin):
    list_filter = [UczelniaFilter]

@admin.register(RodzajCzapki)
class RodzajCzapkiAdmin(BaseModelAdmin):
    filter_horizontal = ['kraje']

register_all_models(
    custom_admins={
        Czapka: CzapkaAdmin,
        RodzajCzapki: RodzajCzapkiAdmin,
    }
)