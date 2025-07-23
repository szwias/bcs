from core.utils.automation.BaseAdmin import *
from .models import ObrazWydarzenie, ObrazZdarzenie, Wydarzenie, Zdarzenie
from .inlines import (
    ZdarzenieInline,
    ObrazWydarzenieInline,
    ObrazZdarzenieInline,
)


@admin.register(ObrazWydarzenie)
class ObrazWydarzenieAdmin(BaseModelAdmin):
    save_as = True
    filter_horizontal = ["widoczne_osoby"]


@admin.register(ObrazZdarzenie)
class ObrazZdarzenieAdmin(BaseModelAdmin):
    save_as = True
    filter_horizontal = ["widoczne_osoby"]


@admin.register(Wydarzenie)
class WydarzenieAdmin(BaseModelAdmin):
    save_as = True
    inlines = [ZdarzenieInline, ObrazWydarzenieInline]
    filter_horizontal = ("miejsca", "uczestnicy")

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
        ObrazWydarzenie: ObrazWydarzenieAdmin,
        ObrazZdarzenie: ObrazZdarzenieAdmin,
        Wydarzenie: WydarzenieAdmin,
        Zdarzenie: ZdarzenieAdmin,
    }
)
