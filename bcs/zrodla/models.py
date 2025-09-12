from PyPDF2.errors import PdfReadError

from django.core.exceptions import ValidationError

from core.utils.Lengths import MAX_LENGTH
from wyszukiwarka.utils.Search import *
from wyszukiwarka.models import SearchableModel, SearchablePolymorphicModel


class Zrodlo(SearchablePolymorphicModel):
    tytul = models.CharField(max_length=MAX_LENGTH, verbose_name="Tytuł")

    autorzy = models.ManyToManyField(
        "osoby.Byt",
        blank=True,
        verbose_name="Autorzy",
        related_name="%(class)s_ktorych_jest_autorem",
    )

    plik = models.FileField(upload_to="pdfs/", blank=True, verbose_name="Plik")

    @property
    def get_autor(self):
        return ", ".join([str(a) for a in self.autorzy.all()])

    class Meta:
        verbose_name = "Źródło"
        verbose_name_plural = "Źródła"
        ordering = ("tytul",)

    def __str__(self):
        autorzy = ", ".join(str(a) for a in self.autorzy.all())
        return f"{self.tytul} | {autorzy}"


class SearchableZrodlo(Zrodlo):
    extracted_text = models.TextField(blank=True, verbose_name="Tekst z pdfa")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.plik:
            try:
                extracted_text = extract_text_from_pdf(self.plik)
                normalized_text = extracted_text.replace("\n", " ").strip()
                self.extracted_text = normalized_text

            except (PdfReadError, OSError, IOError) as e:
                raise ValidationError(f"Could not extract text from PDF: {e}")

        super().save(*args, **kwargs)


class ZrodloOgolne(SearchableZrodlo):
    search_indexable = True

    zawartosc = models.TextField(blank=True, verbose_name="Zawartość")

    gdzie_znalezc = models.TextField(blank=True, verbose_name="Gdzie znaleźć")

    class Meta:
        verbose_name = "Źródło"
        verbose_name_plural = "Źródła różne"
        ordering = ("tytul",)


class Dokument(SearchableZrodlo):
    search_indexable = True

    data = models.DateField(blank=True, null=True, verbose_name="Data wydania")

    streszczenie = models.TextField(
        max_length=MAX_LENGTH, blank=True, verbose_name="Streszczenie"
    )

    class Meta:
        verbose_name = "Dokument"
        verbose_name_plural = "Dokumenty"
        ordering = ["-data"]

    def __str__(self):
        data = self.data or "Data nieznana"
        return f"{self.tytul} - {data}"


class Korespondencja(Dokument):

    adresaci = models.ManyToManyField(
        "osoby.Byt",
        blank=True,
        verbose_name="Adresaci",
    )

    class Meta:
        verbose_name = "Korespondencja"
        verbose_name_plural = "Korespondencja"
        ordering = ["data"]


class Oswiadczenie(Dokument):
    class Meta:
        verbose_name = "Oświadczenie"
        verbose_name_plural = "Oświadczenia"
        ordering = ["-data"]


class Uchwala(Dokument):

    walne = models.ForeignKey(
        "kronika.WydarzenieHistoryczne",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Walne",
    )

    class Meta:
        verbose_name = "Uchwała"
        verbose_name_plural = "Uchwały"
        ordering = ["-data"]


class Rozliczenie(Dokument):

    class Meta:
        verbose_name = "Rozliczenie"
        verbose_name_plural = "Rozliczenia"
        ordering = ["-data"]


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
