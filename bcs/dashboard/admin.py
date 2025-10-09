# dashboard/admin.py
from core.admin_imports import *

from core.admin import register_all_models, BaseModelAdmin
from .models import App


@admin.register(App)
class AppAdmin(BaseModelAdmin):
    list_display = ("nazwa", "opis", "adres_url", "ikona")
    search_fields = ("nazwa", "adres_url")
    list_filter_exclude = "__all__"


register_all_models()
