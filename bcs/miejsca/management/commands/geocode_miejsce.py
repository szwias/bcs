# miejsca/management/commands/geocode_miejsce.py
import time
from django.core.management.base import BaseCommand
from miejsca.models import Miejsce


class Command(BaseCommand):
    """
    Backfill latitude and longitude for Miejsce addresses
    ONLY WITH INTERNET CONNECTION
    """

    def handle(self, *args, **options):
        # Only geocode places without coordinates
        queryset = Miejsce.objects.filter(
            latitude__isnull=True, longitude__isnull=True
        )
        total = queryset.count()
        self.stdout.write(f"Found {total} Miejsce objects to geocode.")

        for i, miejsce in enumerate(queryset.iterator(), start=1):
            self.stdout.write(
                f"[{i}/{total}] Geocoding: {miejsce.nazwa} - {miejsce.adres}"
            )
            result = miejsce.geocode_address()
            if not result:
                self.stdout.write("  -> Failed")
            time.sleep(1)  # Nominatim rate limit
