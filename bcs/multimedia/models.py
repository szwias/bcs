import os

from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel
from core.utils.Search import *

from core.utils.Lengths import MEDIUM_LENGTH


class Obraz(PolymorphicModel):
    tytul = models.CharField(max_length=MEDIUM_LENGTH, verbose_name="Tytuł")

    data = models.DateField(
        default=timezone.now, blank=True, verbose_name="Data wykonania"
    )

    opis = models.TextField(blank=True, verbose_name="Opis")


# Create your models here.
class ObrazZdarzenie(Obraz, SearchableModel):
    zdarzenie = models.ForeignKey(
        "kalendarz.Zdarzenie",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Zdarzenie",
        related_name="zdjecia_ze_zdarzenia",
    )

    miejsce = models.ForeignKey(
        "miejsca.Miejsce",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Miejsce",
        related_name="zdjecia_miejsca",
    )

    obraz = models.ImageField(
        upload_to="images/kalendarz/zdarzenie/", verbose_name="Dodaj obraz"
    )

    widoczne_osoby = models.ManyToManyField(
        "osoby.Osoba",
        blank=True,
        verbose_name="Widoczne osoby",
    )

    class Meta:
        verbose_name = "Zdjęcie ze zdarzenia"
        verbose_name_plural = "Zdjęcia ze zdarzeń"
        ordering = ["-data"]

    def __str__(self):
        image_name = os.path.basename(self.obraz.name)

        if self.zdarzenie:
            name = f"{self.zdarzenie.nazwa} - "
        else:
            name = ""

        if self.tytul:
            name += self.tytul
        else:
            name += image_name

        if self.data:
            name += f" {self.data}"

        return name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if self.zdarzenie:
            self.data = self.zdarzenie.data
            self.miejsce = self.zdarzenie.miejsce
            if is_new:
                for osoba in self.zdarzenie.powiazane_osoby.all():
                    osoba.pk = None
                    osoba.content_object = self
                    osoba.save()

        super().save(*args, **kwargs)


class ObrazWydarzenie(Obraz, SearchableModel):
    wydarzenie = models.ForeignKey(
        "kalendarz.WydarzenieKalendarzowe",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Wydarzenie",
        related_name="zdjecia_z_wydarzenia",
    )

    obraz = models.ImageField(
        upload_to="images/kalendarz/wydarzenie/", verbose_name="Dodaj obraz"
    )

    widoczne_osoby = models.ManyToManyField(
        "osoby.Osoba",
        blank=True,
        verbose_name="Widoczne osoby",
    )

    class Meta:
        verbose_name = "Zdjęcie z wydarzenia"
        verbose_name_plural = "Zdjęcia z wydarzeń"
        ordering = ["-wydarzenie"]

    def __str__(self):
        image_name = os.path.basename(self.obraz.name)
        name = f"{self.wydarzenie.nazwa} - "
        if self.tytul:
            name += self.tytul
        else:
            name += image_name
        return name
