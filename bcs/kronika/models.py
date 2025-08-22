from django.db import models

from core.utils.Consts import MEDIUM_LENGTH, NAME_LENGTH
from core.utils import Czas


class PodsumowanieKadencji(models.Model):

    zarzad = models.ForeignKey(
        "osoby.Zarzad",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Zarząd",
        related_name="podsumowania_kadencji"
    )

    autor = models.ForeignKey(
        "osoby.Czlonek",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Autor",
    )

    podsumowanie = models.TextField(
        blank=True, verbose_name="Podsumowanie kadencji"
    )

    class Meta:
        verbose_name = "Podsumowanie kadencji"
        verbose_name_plural = "Podsumowania kadencji"
        ordering = ["-zarzad"]

    def __str__(self):
        return f"{self.autor}: {self.zarzad.kadencja} ({self.zarzad.wielki_mistrz.imie})"


class Kadencja(models.Model):

    lata = models.IntegerField(choices=Czas.KADENCJE, verbose_name="Lata")

    rozpoczecie = models.ForeignKey(
        "kronika.WydarzenieHistoryczne",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Rozpoczęcie kadencji",
        related_name="rozpoczyna_kadencje",
    )

    zakonczenie = models.ForeignKey(
        "kronika.WydarzenieHistoryczne",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Zakończenie kadencji",
        related_name="konczy_kadencje",
    )

    class Meta:
        verbose_name = "Kadencja"
        verbose_name_plural = "Kadencje"
        ordering = ["lata"]

    def __str__(self):
        return self.get_lata_display()


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

    data = models.DateField(blank=True, null=True, verbose_name="Data")

    opis = models.TextField(blank=True, null=True, verbose_name="Opis")

    wydarzenie = models.ForeignKey(
        "kalendarz.WydarzenieKalendarzowe",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Powiązane wydarzenie z kalendarza",
        related_name="powiazane_wydarzenie_historyczne",
    )

    class Meta:
        verbose_name = "Wydarzenie historyczne"
        verbose_name_plural = "Wydarzenia historyczne"
        ordering = ["nazwa"]

    def __str__(self):
        if str(self.typ).lower() in self.nazwa.lower():
            typ = ""
        else:
            typ = self.typ
        return f'{self.data}: {typ} "{self.nazwa}"'


class ZadanieChrzcielne(models.Model):
    nazwa = models.CharField(
        max_length=NAME_LENGTH, verbose_name="Nazwa krótka"
    )

    autor = models.ForeignKey(
        "osoby.Czlonek",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Autor",
        related_name="zadanie_chrzcielne",
    )

    opis = models.TextField(blank=True, null=True, verbose_name="Opis")

    zalacznik = models.FileField(
        upload_to="pdfs/", blank=True, null=True, verbose_name="Załącznik (pdf)"
    )

    zdjecia = models.ImageField(
        upload_to="images/", blank=True, null=True, verbose_name="Zdjęcia"
    )

    link = models.URLField(blank=True, null=True, verbose_name="Link")

    class Meta:
        verbose_name = "Zadanie chrzcielne"
        verbose_name_plural = "Zadania chrzcielne"
        ordering = ["nazwa"]

    def __str__(self):
        return f"{self.autor} - {self.nazwa}"
