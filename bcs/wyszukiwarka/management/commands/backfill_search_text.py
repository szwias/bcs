# myapp/management/commands/backfill_search_text.py
from django.core.management.base import BaseCommand
from core.models import SearchableModel
from django.apps import apps


class Command(BaseCommand):
    help = "Backfill the search_text field for all SearchableModel records."

    def handle(self, *args, **options):
        # Get all subclasses dynamically
        for model in apps.get_models():
            if issubclass(model, SearchableModel) and not model._meta.abstract:
                self.stdout.write(f"Updating {model.__name__}...")
                for obj in model.objects.all().iterator():
                    obj.save(
                        update_fields=["search_text"]
                    )  # triggers save() logic
                self.stdout.write(
                    self.style.SUCCESS(f"Done: {model.__name__}")
                )
