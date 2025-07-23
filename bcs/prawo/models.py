from django.db import models
from polymorphic.models import PolymorphicModel

from core.utils.Consts import MAX_LENGTH, NAME_LENGTH


class Podmiot(PolymorphicModel):
    nazwa = models.CharField(max_length=NAME_LENGTH, verbose_name="Nazwa")

    class Meta:
        verbose_name = "Podmiot"
        verbose_name_plural = "Podmioty"
        ordering = ["nazwa"]

    def __str__(self):
        return self.nazwa


class Rola(Podmiot):
    class Meta:
        verbose_name = "Rola jednostki w Bractwie"
        verbose_name_plural = "Role jednostki w Bractwie"
        ordering = ["nazwa"]


class Struktura(Podmiot):
    class Meta:
        verbose_name = "Struktura w Bractwie"
        verbose_name_plural = "Struktury w Bractwie"
        ordering = ["nazwa"]


class RelacjaPrawna(models.Model):
    class Wybory(models.TextChoices):
        PRAWO = "P", "Prawo"
        OBOWIAZEK = "O", "Obowiązek"

    tytul = models.CharField(max_length=MAX_LENGTH, verbose_name="Tytuł")

    podmiot = models.ManyToManyField(
        Podmiot, blank=True, verbose_name="Podmiot"
    )

    prawo_czy_obowiazek = models.CharField(
        max_length=1, choices=Wybory.choices, verbose_name="Rodzaj relacji"
    )

    dokument = models.ForeignKey(
        "dokumenty.Dokument",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Dokument",
    )

    class Meta:
        verbose_name = "Relacja prawna"
        verbose_name_plural = "Prawa i obowiązki"
        ordering = ["tytul"]

    def __str__(self):
        return self.tytul
