from django.db import models
from polymorphic.models import PolymorphicModel

from core.utils.Consts import MAX_LENGTH


# Create your models here.
class Dokument(PolymorphicModel):
    tytul = models.CharField(max_length=MAX_LENGTH, verbose_name="Tytuł")

    data = models.DateField(blank=True, verbose_name="Data wydania")

    streszczenie = models.TextField(blank=True, verbose_name="Streszczenie")

    autorzy = models.ManyToManyField(
        "osoby.Osoba",
        blank=True,
        verbose_name="Autorzy",
        related_name="wydane_dokumenty",
    )

    plik = models.FileField(
        upload_to="pdfs/", blank=True, verbose_name="Tekst"
    )

class ZrodloOgolne(models.Model):

    zawartosc = models.TextField(blank=True, verbose_name="Zawartość")

    gdzie_znalezc = models.TextField(blank=True, verbose_name="Gdzie znaleźć")

    class Meta:
        verbose_name = "Źródło"
        verbose_name_plural = "Źródła różne"
        ordering = ("tytul",)


    class Meta:
        verbose_name = "Dokument"
        verbose_name_plural = "Dokumenty"
        ordering = ["-data"]

    def __str__(self):
        return f"{self.tytul} - {self.data}"


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
