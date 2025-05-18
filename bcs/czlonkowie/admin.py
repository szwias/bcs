from core.utils.automation.BaseAdmin import *
from .models import DawnyZarzad, Zarzad, HallOfFame, ImieSzlacheckie, Osoby, WielkiMistrz, ZwierzeCzapkowe


@admin.register(DawnyZarzad)
class DawnyZarzadAdmin(BaseModelAdmin):
    list_filter_exclude = "__all__"

@admin.register(HallOfFame)
class HallOfFameAdmin(BaseModelAdmin):
    list_filter_exclude = "__all__"

@admin.register(ImieSzlacheckie)
class ImieSzlacheckieAdmin(BaseModelAdmin):
    list_filter_exclude = "__all__"

@admin.register(Osoby)
class OsobyAdmin(BaseModelAdmin):
    list_filter_exclude = ["content_type"]

@admin.register(WielkiMistrz)
class WielkiMistrzAdmin(BaseModelAdmin):
    list_filter_exclude = "__all__"

@admin.register(ZwierzeCzapkowe)
class ZwierzeCzapkoweAdmin(BaseModelAdmin):
    list_filter_exclude = "__all__"

register_all_models(
    custom_admins={
        DawnyZarzad: DawnyZarzadAdmin,
        HallOfFame: HallOfFameAdmin,
        ImieSzlacheckie: ImieSzlacheckieAdmin,
        Osoby: OsobyAdmin,
        WielkiMistrz: WielkiMistrzAdmin,
        ZwierzeCzapkowe: ZwierzeCzapkoweAdmin,
    }
)