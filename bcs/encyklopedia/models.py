from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from core.utils.Choices import IntAlt
from core.utils.Consts import *
from core.utils.czas import Czas
from kronika.models import Wydarzenie


class Lengths:
    OKOLICZNOSCI_LENGTH = 3
    PANSTWA_LENGTH = 3
    CZAPKI_LENGTH = 3

# Create your models here.
class TradycjaBCS(models.Model):
    class Authors(models.TextChoices):
        BELGOWIE = "Belg", "Belgijska"
        BCS = "BCS", "BCSu"
        FALUSZARDZI = "Faluch", "Faluszardzka"
        GOLIARDZI = "Goliard", "Goliardzka"
        INNE = "Inne", "Inna"
        KORPORACJE = "Korpo", "Korporacyjna"

    class Okolicznosci(models.TextChoices):
        INNE = "I", "Inne"
        WYDARZENIE = "Wyd", "Wydarzenie"

    nazwa = models.CharField(
        max_length=MEDIUM_LENGTH, verbose_name="Nazwa",
    )

    autor_rodzaj = models.CharField(
        max_length=SHORT_LENGTH,
        choices=Authors.choices,
        default=Authors.BCS,
        verbose_name="Tradycja",
    )

    autor = GenericRelation(
        "czlonkowie.Osoby", blank=True,  verbose_name="Autor", related_name="zaczete_tradycje"
    )

    okolicznosci_powstania = models.CharField(
        max_length=Lengths.OKOLICZNOSCI_LENGTH, choices=Okolicznosci.choices, verbose_name="Okoliczności powstania",
    )

    wydarzenie = models.ForeignKey(
        Wydarzenie,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Wydarzenie",
        related_name="tradycje_zapoczatkowane_wydarzeniem"
    )

    inne = models.CharField(
        max_length=MAX_LENGTH, blank=True, verbose_name="Inna okoliczność (wpisz)",
    )

    opis = models.TextField(
        blank=True, verbose_name="Opis",
    )

    class Meta:
        verbose_name = "Tradycja BCS"
        verbose_name_plural = "Tradycje BCS"
        ordering = ("nazwa",)

    def __str__(self):
        return self.nazwa

class TradycjaInnegoBractwa(models.Model):
    class Authors(models.TextChoices):
        ANIMUS = "Animus", "BCS Animus"
        BELGOWIE = "Belg", "Belgijska"
        FALUSZARDZI = "Faluch", "Faluszardzka"
        GOLIARDZI = "Goliard", "Goliardzka"
        INNE = "Inne", "Inna"
        KORPORACJE = "Korpo", "Korporacyjna"

    nazwa = models.CharField(
        max_length=MEDIUM_LENGTH,
        verbose_name="Nazwa",
    )

    autor_rodzaj = models.CharField(
        max_length=SHORT_LENGTH,
        choices=Authors.choices,
        verbose_name="Pochodzenie tradycji",
    )

    opis = models.TextField(
        blank=True,
        verbose_name="Opis",
    )

    class Meta:
        verbose_name = "Tradycja innego bractwa"
        verbose_name_plural = "Tradycje innych bractw"
        ordering = ("nazwa",)

    def __str__(self):
        return self.nazwa

class Bractwo(models.Model):
    class Panstwa(models.TextChoices):
        BELGIA = "BEL", "Belgia"
        DANIA = "DNK", "Dania"
        FINLANDIA = "FIN", "Finlandia"
        FRANCJA = "FRA", "Francja"
        NIEMCY = "DEU", "Niemcy"
        NORWEGIA = "NOR", "Norwegia"
        POLSKA = "POL", "Polska"
        SZWECJA = "SWE", "Szwecja"
        WLOCHY = "ITA", "Włochy"

    class Czapki(models.TextChoices):
        CALOTTE = "CAL", "Calotte"
        CZAPKA = "CZA", "Czapka"
        FALUCH = "FAL", "Faluch"
        FELUCA = "FEL", "Feluca"
        INNA = "I", "Inna"


    nazwa = models.CharField(
        max_length=MAX_LENGTH, verbose_name="Nazwa",
    )

    panstwo = models.CharField(
        max_length=Lengths.PANSTWA_LENGTH, choices=Panstwa.choices, verbose_name="Kraj pochodzenia",
    )

    czapka = models.CharField(
        max_length=Lengths.CZAPKI_LENGTH, choices=Czapki.choices, verbose_name="Czapka",
    )

    rok_zalozenia = models.IntegerField(
        choices=Czas.LATA_BRACTW + [IntAlt.DONT_KNOW], default=IntAlt.DONT_KNOW, verbose_name="Rok założenia",
    )

    wiek_tradycje = models.IntegerField(
        choices=Czas.WIEKI + [IntAlt.DONT_KNOW], default=IntAlt.DONT_KNOW, verbose_name="Tradycje sięgają którego wieku",
    )

    class Meta:
        verbose_name = "Bractwo"
        verbose_name_plural = "Bractwa"
        ordering = ["panstwo", "nazwa"]

    def __str__(self):
        return f"{self.panstwo} {self.nazwa}"


# class Pojecie(models.Model):
#     class Origins(models.TextChoices):
#         INNE = "Inne", "Inna okoliczność"
#         WYDARZENIE = "Wydarzenie", "Na wydarzeniu czapkowym"
#         WYJAZD = "Wyjazd", "Na wyjeździe"
#
#     class Autorzy
#
#     nazwa = models.CharField(
#         max_length=MEDIUM_LENGTH,
#         verbose_name="Nazwa",
#     )
#
#     opis = models.TextField(
#         blank=True,
#         verbose_name="Opis",
#     )
#
#     origins = models.CharField(
#         blank=True,
#         choices=Origins.choices,
#         verbose_name="Pierwszy raz pojawiło się:",
#     )
#
#     wydarzenie = models.ForeignKey(
#         Wydarzenie,
#         blank=True,
#         null=True,
#         on_delete=models.SET_NULL,
#         verbose_name="Wydarzenie",
#     )
#
#     wyjazd = models.ForeignKey(
#         Wyjazd,
#         blank=True,
#         null=True,
#         on_delete=models.SET_NULL,
#         verbose_name="Wyjazd",
#     )
#
#     autorem = models.CharField(
#
#     )