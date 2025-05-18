from .utils.automation.BaseAdmin import *

from .utils.czas.models import Kadencja

@admin.register(Kadencja)
class KadencjaAdmin(BaseModelAdmin):
    list_filter_exclude = "__all__"


register_all_models(
    custom_admins={
        Kadencja: KadencjaAdmin,
    }
)
