from core.utils.automation.BaseAdmin import *
from .models import RodzajCzapki

@admin.register(RodzajCzapki)
class RodzajCzapkiAdmin(BaseModelAdmin):
    filter_horizontal = ['kraje']

register_all_models(
    custom_admins={
        RodzajCzapki: RodzajCzapkiAdmin,
    }
)