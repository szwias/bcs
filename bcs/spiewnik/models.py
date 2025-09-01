from django.db import models

from core.utils.Lengths import MAX_LENGTH, MEDIUM_LENGTH


class KategoriaPiosenki(models.Model):

    nazwa = models.CharField(
        max_length=MEDIUM_LENGTH, verbose_name="Nazwa kategorii"
    )

    class Meta:
        verbose_name = "Kategoria piosenki"
        verbose_name_plural = "Kategorie piosenek"
        ordering = ["nazwa"]

    def __str__(self):
        return self.nazwa


class Piosenka(models.Model):

    tytul = models.CharField(max_length=MAX_LENGTH, verbose_name="Tytuł")

    autor = models.CharField(
        max_length=MAX_LENGTH, blank=True, verbose_name="Autor"
    )

    znani_czapce_autorzy = models.ManyToManyField(
        "osoby.Osoba",
        blank=True,
        verbose_name="Znani BCS autorzy",
    )

    kategorie = models.ManyToManyField(
        "spiewnik.KategoriaPiosenki",
        blank=True,
        verbose_name="Kategoria piosenki",
    )

    tekst = models.FileField(
        upload_to="piosenki/",
        blank=True,
        help_text="""
        Dodaj tekst w formacie .json, przykład:
        [
          {"tekst": "Tekst wiersza", "chwyty": ["C", "D"]}, 
          {"tekst": "Tekst wiersza", "chwyty": ["G", "D"]},
          {"tekst": "", "chwyty": []},
          {"tekst": "Po ostatniej linii nie dajemy przecinka", "chwyty": ["Am"]}
        ]
        """,
        verbose_name="Tekst w formacie .json",
    )

    tekst_alternatywny = models.FileField(
        upload_to="piosenki/",
        blank=True,
        help_text="""
        Dodaj tekst w formacie .json, przykład:
        [
          {"tekst": "Tekst wiersza", 
           "chwyty": ["C", "D"]}, 
          {"tekst": "Tekst wiersza", 
           "chwyty": ["G", "D"]},
          {"tekst": "", 
           "chwyty": []},
          {"tekst": "Po ostatniej linii nie dajemy przecinka", 
           "chwyty": ["Am"]}
        ]
        """,
        verbose_name="Tekst alternatywny (np. tłumaczenie) w formacie .json",
    )

    class Meta:
        verbose_name = "Piosenka"
        verbose_name_plural = "Piosenki"
        ordering = ["tytul"]

    def __str__(self):
        return self.tytul
