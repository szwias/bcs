from django.db import models
from polymorphic.models import PolymorphicModel

from core.utils.Consts import MAX_LENGTH


class Zrodlo(PolymorphicModel):
    tytul = models.CharField(
        max_length=MAX_LENGTH, verbose_name="Tytuł"
    )

    autorzy = models.ManyToManyField(
        "osoby.Osoba",
        blank=True,
        verbose_name="Autorzy",
        related_name="%(class)s_ktorych_jest_autorem",
    )

    plik = models.FileField(upload_to="pdfs/", blank=True, verbose_name="Plik")

    class Meta:
        verbose_name = "Źródło"
        verbose_name_plural = "Źródła"
        ordering = ("tytul",)

    def __str__(self):
        autorzy = ", ".join(a for a in self.autorzy.all())
        return f"{self.tytul} | {autorzy}"


class ZrodloOgolne(Zrodlo):

    zawartosc = models.TextField(blank=True, verbose_name="Zawartość")

    gdzie_znalezc = models.TextField(blank=True, verbose_name="Gdzie znaleźć")

    class Meta:
        verbose_name = "Źródło"
        verbose_name_plural = "Źródła różne"
        ordering = ("tytul",)


class Dokument(Zrodlo):

    data = models.DateField(blank=True, null=True, verbose_name="Data wydania")

    streszczenie = models.TextField(
        max_length=MAX_LENGTH, blank=True, verbose_name="Streszczenie"
    )

    class Meta:
        verbose_name = "Dokument"
        verbose_name_plural = "Dokumenty"
        ordering = ["-data"]

    def __str__(self):
        data = self.data or ""
        streszczenie = " (" + str(self.streszczenie) + ")" if self.streszczenie else ""
        return f"{self.tytul} - {data}{streszczenie}"


class Edykt(Dokument):
    numer = models.IntegerField(blank=True, null=True, verbose_name="Numer")

    class Meta:
        verbose_name = "Edykt"
        verbose_name_plural = "Edykty"
        ordering = ["-numer"]


class Ukaz(Dokument):
    numer = models.IntegerField(blank=True, null=True, verbose_name="Numer")

    class Meta:
        verbose_name = "Ukaz"
        verbose_name_plural = "Ukazy"
        ordering = ["-numer"]
