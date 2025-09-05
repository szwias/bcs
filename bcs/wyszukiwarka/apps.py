# wyszukiwarka/apps.py
from django.apps import AppConfig

from .registry import register_search


class WyszukiwarkaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wyszukiwarka"

    def ready(self):
        apps_to_index = [
            "czapki",
            "encyklopedia",
            "honory",
            "kalendarz",
            "kronika",
            "miejsca",
            "multimedia",
            "osoby",
            "prawo",
            "skarbiec",
            "slowniczek_lacinski",
            "zrodla",
        ]
        register_search(apps_to_index)
