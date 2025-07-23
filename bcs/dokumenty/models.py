from django.db import models
from polymorphic.models import PolymorphicModel

from core.utils.Consts import MAX_LENGTH


# Create your models here.
class Dokument(PolymorphicModel):
    tytul = models.CharField(max_length=MAX_LENGTH, verbose_name="Tytuł")

    data = models.DateField(
        auto_now_add=True, blank=True, verbose_name="Data wydania"
    )

    streszczenie = models.CharField(
        max_length=MAX_LENGTH, blank=True, verbose_name="Streszczenie"
    )

    autorzy = models.ManyToManyField(
        "osoby.Osoba",
        blank=True,
        verbose_name="Autorzy",
        related_name="wydane_dokumenty",
    )

    tekst = models.TextField(blank=True, verbose_name="Tekst")

    class Meta:
        verbose_name = "Dokument"
        verbose_name_plural = "Dokumenty"
        ordering = ["-data"]


class Edykt(Dokument):
    numer = models.IntegerField(blank=True, verbose_name="Numer")

    class Meta:
        verbose_name = "Edykt"
        verbose_name_plural = "Edykty"
        ordering = ["-numer"]


class Ukaz(Dokument):
    numer = models.IntegerField(blank=True, verbose_name="Numer")

    class Meta:
        verbose_name = "Ukaz"
        verbose_name_plural = "Ukazy"
        ordering = ["-numer"]
