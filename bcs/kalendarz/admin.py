from core.utils.Czas import ROK_ZALOZENIA, BIEZACY_ROK
from core.utils.automation.BaseAdmin import (
    admin,
    BaseModelAdmin,
    register_all_models,
)
from kalendarz.models import (
    Zdarzenie,
    WydarzenieKalendarzowe,
    Wydarzenie,
    DepositioBeanorum,
)
from .inlines import ZdarzenieInline
from .filters import YearListFilter
from multimedia.inlines import ObrazWydarzenieInline, ObrazZdarzenieInline


@admin.register(DepositioBeanorum)
class DepositioBeanorumAdmin(BaseModelAdmin):
    save_as = True
    filter_horizontal = ["chrzczeni"]
    list_filter_exclude = ["polymorphic_ctype", "wydarzeniekalendarzowe_ptr"]


@admin.register(WydarzenieKalendarzowe)
class WydarzenieKalendarzoweAdmin(BaseModelAdmin):
    save_as = True
    hide_base_class_from_index = False
    list_filter = [YearListFilter]


@admin.register(Wydarzenie)
class WydarzenieAdmin(BaseModelAdmin):
    save_as = True
    inlines = [ZdarzenieInline, ObrazWydarzenieInline]
    filter_horizontal = ("miejsca", "uczestnicy")
    list_filter = [
        YearListFilter,
        "czy_jednodniowe",
        "czy_to_wyjazd",
        "typ_wydarzenia",
        "typ_wyjazdu",
        "miejsca",
    ]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        # Save each inline instance
        for instance in instances:
            instance.wydarzenie = form.instance
            instance.save()

        # Save M2M if needed
        formset.save_m2m()

        # Collect miejsca from all Zdarzenie inlines
        if formset.model == Zdarzenie:
            miejsca_set = {
                z.miejsce
                for z in form.instance.zdarzenia_z_wydarzenia.all()
                if z.miejsce
            }
            form.instance.miejsca.add(
                *miejsca_set
            )  # Replace all current with new set


@admin.register(Zdarzenie)
class ZdarzenieAdmin(BaseModelAdmin):
    inlines = [ObrazZdarzenieInline]
    filter_horizontal = ["powiazane_osoby"]
    save_as = True


register_all_models(
    custom_admins={
        DepositioBeanorum: DepositioBeanorumAdmin,
        Wydarzenie: WydarzenieAdmin,
        WydarzenieKalendarzowe: WydarzenieKalendarzoweAdmin,
        Zdarzenie: ZdarzenieAdmin,
    }
)
