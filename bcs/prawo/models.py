from django.db import models

from core.utils.Consts import MAX_LENGTH, NAME_LENGTH


class Dokument(models.Model):
    tytul = models.CharField(max_length=MAX_LENGTH, verbose_name="Tytuł")

    data = models.DateField(auto_now_add=True, verbose_name="Data wydania")

    streszczenie = models.CharField(
        max_length=MAX_LENGTH, blank=True, verbose_name="Streszczenie"
    )

    autorzy = models.ManyToManyField(
        "osoby.Osoba",
        blank=True,
        verbose_name="Autorzy",
        related_name="wydane_dokumenty",
    )

    tekst = models.TextField(verbose_name="Tekst")

    class Meta:
        verbose_name = "Dokument"
        verbose_name_plural = "Dokumenty"
        ordering = ["-data"]


class Edykt(Dokument):
    class Meta:
        verbose_name = "Edykt"
        verbose_name_plural = "Edykty"
        ordering = ["-data"]


class Ukaz(Dokument):
    class Meta:
        verbose_name = "Ukaz"
        verbose_name_plural = "Ukazy"
        ordering = ["-data"]


class Podmiot(models.Model):
    nazwa = models.CharField(max_length=NAME_LENGTH, verbose_name="Nazwa")

    class Meta:
        verbose_name = "Podmiot"
        verbose_name_plural = "Podmioty"
        ordering = ["nazwa"]

    def __str__(self):
        return self.nazwa


class RelacjaPrawna(models.Model):
    tytul = models.CharField(max_length=MAX_LENGTH, verbose_name="Tytuł")

    podmiot = models.ManyToManyField(
        Podmiot, blank=True, verbose_name="Podmiot"
    )

    class Meta:
        abstract = True


class Prawo(RelacjaPrawna):
    class Meta:
        verbose_name = "Prawo"
        verbose_name_plural = "Prawa"
        ordering = ["tytul"]

    def __str__(self):
        return self.tytul


class Obowiazek(RelacjaPrawna):
    class Meta:
        verbose_name = "Obowiązek"
        verbose_name_plural = "Obowiązki"
        ordering = ["tytul"]
