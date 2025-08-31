from django.db import models
from polymorphic.models import PolymorphicModel

from core.utils.Consts import MAX_LENGTH, NAME_LENGTH


class DlugoscKadencji(models.Model):
    okres = models.CharField(
        max_length=MAX_LENGTH, verbose_name="Długość kadencji"
    )

    class Meta:
        verbose_name = "Długość kadencji"
        verbose_name_plural = "Długości kadencji"
        ordering = ["okres"]

    def __str__(self):
        return self.okres


class WielkoscStruktury(models.Model):
    wielkosc = models.CharField(
        max_length=MAX_LENGTH, verbose_name="Wielkość"
    )

    class Meta:
        verbose_name = "Wielkosc"
        verbose_name_plural = "Wielkosc"
        ordering = ["wielkosc"]

    def __str__(self):
        return self.wielkosc


class Podmiot(PolymorphicModel):
    nazwa = models.CharField(max_length=NAME_LENGTH, verbose_name="Nazwa")

    aktualne = models.BooleanField(default=True, verbose_name="Aktualne")

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

    tresc = models.TextField(max_length=MAX_LENGTH, verbose_name="Treść")

    prawo_czy_obowiazek = models.CharField(
        max_length=1, choices=Wybory.choices, verbose_name="Rodzaj relacji"
    )

    class Meta:
        verbose_name = "Relacja prawna"
        verbose_name_plural = "Prawa i obowiązki"
        ordering = ["tresc"]

    def __str__(self):
        return self.tresc


class PrawoObowiazek(models.Model):
    podmiot = models.ForeignKey(
        Podmiot,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Podmiot",
    )

    relacja = models.ForeignKey(
        RelacjaPrawna,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Prawo/Obowiązek",
    )

    aktualne = models.BooleanField(
        default=True, verbose_name="Aktualne"
    )

    dokument = models.ForeignKey(
        "zrodla.Dokument",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Dokument",
    )

    class Meta:
        verbose_name = "Prawo/Obowiązek"
        verbose_name_plural = "Kodeks"
        ordering = ["podmiot", "relacja"]

    def __str__(self):
        aktualne = "" if self.aktualne else " - NIEAKTUALNE"
        return f"{self.podmiot}: {self.relacja}{aktualne}"
