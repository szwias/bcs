from django.db import models
from core.utils.czas import Czas


class Kadencja(models.Model):
    rozpoczecie = models.IntegerField(
        choices=Czas.LATA_BCS,
        verbose_name="Rozpoczęcie",
    )

    zakonczenie = models.IntegerField(
        blank=True,
        verbose_name="Zakonczenie",
    )

    class Meta:
        verbose_name = "Kadencja"
        verbose_name_plural = "Kadencje"
        ordering = ['rozpoczecie']

    def __str__(self):
        return f"{self.rozpoczecie}/{self.zakonczenie}"