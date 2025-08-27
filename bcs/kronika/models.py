from django.db import models

from core.utils.Consts import MEDIUM_LENGTH, NAME_LENGTH
from core.utils import Czas


class PodsumowanieKadencji(models.Model):

    zarzad = models.ForeignKey(
        "osoby.Zarzad",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Zarząd",
        related_name="podsumowania_kadencji",
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

    typy = models.ManyToManyField(
        TypWydarzeniaHistorycznego,
        blank=True,
        verbose_name="Typ wydarzenia historycznego",
    )

    data_przyblizona = models.CharField(
        max_length=MEDIUM_LENGTH,
        blank=True,
        null=True,
        verbose_name="Data przybliżona",
    )

    opis = models.TextField(blank=True, null=True, verbose_name="Opis")

    wydarzenie = models.ForeignKey(
        "kalendarz.WydarzenieKalendarzowe",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Powiązane wydarzenie z kalendarza",
        related_name="powiazane_wydarzenie_historyczne",
    )

    dokument = models.ForeignKey(
        "zrodla.Dokument",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Powiązany dokument",
    )

    pojecie = models.ForeignKey(
        "encyklopedia.Pojecie",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Link do pojęcia ze słownika",
    )

    class Meta:
        verbose_name = "Wydarzenie historyczne"
        verbose_name_plural = "Wydarzenia historyczne"
        ordering = ["-wydarzenie__data_rozpoczecia", "-data_przyblizona"]

    @property
    def get_data(self):
        return (
            self.wydarzenie.data_rozpoczecia
            if self.wydarzenie
            else self.data_przyblizona
        )

    @property
    def get_types(self):
        return ", ".join([str(t) for t in self.typy.all()])

    def __str__(self):
        if str(self.get_types).lower() in self.nazwa.lower():
            typ = ""
        else:
            typ = str(self.get_types)

        nazwa = str(self.nazwa)
        words = typ.lower().split()
        nazwa_lower = nazwa.lower()

        # check every contiguous subsequence of words
        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                seq = " ".join(words[i:j])
                if seq and seq in nazwa_lower:
                    typ = ""
                    break
            if typ == "":
                break

        return f'{self.get_data}: {typ} "{self.nazwa}"'


class KategoriaZadaniaChrzcielnego(models.Model):
    nazwa = models.CharField(max_length=MEDIUM_LENGTH, verbose_name="Nazwa")

    class Meta:
        verbose_name = "Kategoria zadania chrzcielnego"
        verbose_name_plural = "Kategorie zadań chrzcielnych"
        ordering = ["nazwa"]

    def __str__(self):
        return self.nazwa


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

    kategoria = models.ForeignKey(
        KategoriaZadaniaChrzcielnego,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Kategoria",
    )

    opis = models.TextField(blank=True, null=True, verbose_name="Opis")

    zalacznik = models.FileField(
        upload_to="pdfs/",
        blank=True,
        null=True,
        verbose_name="Załącznik (pdf)",
    )

    zdjecia = models.ImageField(
        upload_to="images/", blank=True, null=True, verbose_name="Zdjęcia"
    )

    link = models.URLField(blank=True, null=True, verbose_name="Link")

    class Meta:
        verbose_name = "Zadanie chrzcielne"
        verbose_name_plural = "Zadania chrzcielne"
        ordering = ["-autor__depositio_beanorum__data_rozpoczecia"]

    def __str__(self):
        return f"{self.autor} - {self.nazwa} - {self.kategoria}"
