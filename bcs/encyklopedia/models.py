from django.db import models
from core.utils.Consts import *
from kronika.models import Wydarzenie, Wyjazd


# Create your models here.
class Tradycja(models.Model):
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
        WYJAZD = "Wyj", "Wyjazd"

    nazwa = models.CharField(
        max_length=MEDIUM_LENGTH,
        verbose_name="Nazwa",
    )

    autor_rodzaj = models.CharField(
        max_length=10,
        choices=Authors.choices,
        default=Authors.BCS,
        verbose_name="Tradycja",
    )

    okolicznosci_powstania = models.CharField(
        max_length=3,
        choices=Okolicznosci.choices,
        verbose_name="Okoliczności powstania",
    )

    wydarzenie = models.ForeignKey(
        Wydarzenie,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Wydarzenie",
    )

    wyjazd = models.ForeignKey(
        Wyjazd,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Wyjazd",
    )

    inne = models.CharField(
        max_length=MAX_LENGTH,
        blank=True,
        verbose_name="Inna okoliczność (wpisz)",
    )

    opis = models.TextField(
        blank=True,
        verbose_name="Opis",
    )

    class Meta:
        verbose_name = "Tradycja"
        verbose_name_plural = "Tradycje"
        ordering = ("nazwa",)

    def __str__(self):
        return self.nazwa

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