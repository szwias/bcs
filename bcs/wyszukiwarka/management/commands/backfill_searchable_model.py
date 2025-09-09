# myapp/management/commands/backfill_searchable_model.py
from django.core.management.base import BaseCommand
from wyszukiwarka.models import SearchableModel
from django.apps import apps


class Command(BaseCommand):
    help = "Backfill the search_text field for all SearchableModel records."

    def handle(self, *args, **options):
        # Get all subclasses dynamically
        for model in apps.get_models():
            if issubclass(model, SearchableModel) and not model._meta.abstract:
                for obj in model.objects.all().iterator():
                    obj.save(
                        update_fields=[
                            "search_dict",
                            "tsv",
                        ]
                    )  # triggers save() logic
