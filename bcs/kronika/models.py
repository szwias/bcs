from django.db import models

from core.utils.Consts import MEDIUM_LENGTH, NAME_LENGTH


class CharakterystykaDzialanZarzadu(models.Model):
    zarzad = models.ForeignKey(
        "osoby.Zarzad",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Zarząd",
    )

    dawny_zarzad = models.ForeignKey(
        "osoby.DawnyZarzad",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Dawny Zarząd",
    )

    autor = models.ForeignKey(
        "osoby.Czlonek",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Autor",
    )

    charakterystyka = models.TextField(
        blank=True, verbose_name="Charakterystyka działań Zarządu"
    )

    class Meta:
        verbose_name = "Charakterystyka działań Zarządu"
        verbose_name_plural = "Charakterystyki działań Zarządów"
        ordering = ["-zarzad"]

    def __str__(self):
        return f"{self.autor}: {self.zarzad.kadencja if self.zarzad else self.dawny_zarzad.kadencja}"


class TypWydarzeniaHistorycznego(models.Model):
    typ = models.CharField(
        max_length=NAME_LENGTH, verbose_name="Typ wydarzenia historycznego"
    )

    class Meta:
        verbose_name = "Typ wydarzenia historycznego"
        verbose_name_plural = "Typy wydarzeń historycznych"
        ordering = ["typ"]

    def __str__(self):
        return self.typ


class WydarzenieHistoryczne(models.Model):
    nazwa = models.CharField(max_length=MEDIUM_LENGTH, verbose_name="Nazwa")

    typ = models.ForeignKey(
        TypWydarzeniaHistorycznego,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Typ wydarzenia historycznego",
    )

    data = models.DateField(blank=True, verbose_name="Data")

    opis = models.TextField(blank=True, verbose_name="Opis")

    class Meta:
        verbose_name = "Wydarzenie historyczne"
        verbose_name_plural = "Wydarzenia historyczne"
        ordering = ["nazwa"]

    def __str__(self):
        return f'{self.data}: {self.typ} "{self.nazwa}"'
