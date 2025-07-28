from django.db import models
from polymorphic.models import PolymorphicModel

from core.utils.Choices import IntAlt
from core.utils.Consts import *
from core.utils import Czas
from kalendarz.models import Wydarzenie


class Lengths:
    OKOLICZNOSCI_LENGTH = 3


class Okolicznosci(models.TextChoices):
    DOKUMENT = "Dok", "W dokumencie"
    INNE = "I", "Inne okoliczności"
    WYDARZENIE = "Wyd", "Na wydarzeniu czapkowym"


class Bractwo(models.Model):

    nazwa = models.CharField(max_length=MAX_LENGTH, verbose_name="Nazwa")

    panstwo = models.ForeignKey(
        "miejsca.Kraj",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Kraj pochodzenia",
    )

    grupa_bractw = models.ForeignKey(
        "encyklopedia.GrupaBractw",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Grupa bractw",
    )

    zalozyciele = models.ManyToManyField(
        "osoby.Osoba", blank=True, verbose_name="Założyciele"
    )

    rok_zalozenia = models.IntegerField(
        choices=Czas.LATA_BRACTW + [IntAlt.DONT_KNOW],
        default=IntAlt.DONT_KNOW,
        verbose_name="Rok założenia",
    )

    wiek_tradycje = models.IntegerField(
        choices=Czas.WIEKI + [IntAlt.DONT_KNOW],
        default=IntAlt.DONT_KNOW,
        verbose_name="Tradycje sięgają którego wieku",
    )

    class Meta:
        verbose_name = "Bractwo"
        verbose_name_plural = "Bractwa"
        ordering = ["panstwo", "nazwa"]

    def __str__(self):
        return f"{str(self.panstwo)}: {self.nazwa}"


class Cytat(PolymorphicModel):
    tekst = models.TextField(verbose_name="Tekst")

    kontekst = models.TextField(blank=True, verbose_name="Kontekst")

    zrodlo = models.ForeignKey(
        "zrodla.Zrodlo",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Źródło",
    )

    autor = models.ForeignKey(
        "osoby.Byt",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Autor",
    )

    adresaci = models.ManyToManyField(
        "osoby.Osoba",
        blank=True,
        verbose_name="Adresat/adresaci powiedzenia",
        related_name="zwiazane_zen_powiedzenia",
    )

    class Meta:
        verbose_name = "Cytat"
        verbose_name_plural = "Cytaty"
        ordering = ("tekst",)

    def __str__(self):
        tekst = str(self.tekst)
        kontekst = str(self.kontekst)
        short_tekst = (
            f"\"{tekst if len(tekst) <= 100 else tekst[:100] + '...'}\""
        )
        adresaci = ", ".join(str(a) for a in self.adresaci.all())
        adresat_str = f" do {adresaci}" if adresaci else ""
        kontekst = f"{' (' + kontekst + ')' if kontekst and len(kontekst) <= 100 else ''}"
        return f"{short_tekst} - {self.autor}{adresat_str}{kontekst}"


class Aforyzm(Cytat):

    class Meta:
        verbose_name = "Aforyzm"
        verbose_name_plural = "Aforyzmy"
        ordering = ["tekst"]


class Powiedzenie(Cytat):

    class Meta:
        verbose_name = "Powiedzenie"
        verbose_name_plural = "Powiedzenia"
        ordering = ["tekst"]


class GrupaBractw(models.Model):
    nazwa = models.CharField(max_length=NAME_LENGTH, verbose_name="Nazwa")

    kraje = models.ManyToManyField(
        "miejsca.Kraj", blank=True, verbose_name="Kraje"
    )

    opis = models.TextField(blank=True, verbose_name="Opis")

    rodzaj_czapki = models.ForeignKey(
        "czapki.RodzajCzapki",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Rodzaj czapki",
    )

    class Meta:
        verbose_name = "Grupa bractw"
        verbose_name_plural = "Grupy bractw"
        ordering = ["nazwa"]

    def __str__(self):
        kraje = ", ".join(str(k) for k in self.kraje.all())
        return f"{self.nazwa}: {kraje}"


class Pojecie(models.Model):

    nazwa = models.CharField(max_length=MEDIUM_LENGTH, verbose_name="Nazwa")

    complete = models.BooleanField(default=False, verbose_name="Notatka kompletna")

    autor = models.ForeignKey(
        "osoby.Byt",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Autor pojęcia",
    )

    opis = models.TextField(blank=True, verbose_name="Opis")

    origins = models.CharField(
        blank=True,
        choices=Okolicznosci.choices,
        verbose_name="Pierwszy raz pojawiło się:",
    )

    wydarzenie = models.ForeignKey(
        Wydarzenie,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Wydarzenie",
    )

    zrodlo = models.ForeignKey(
        "zrodla.Zrodlo",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Źródło"
    )

    class Meta:
        verbose_name = "Pojęcie"
        verbose_name_plural = "Pojęcia"
        ordering = ("nazwa",)

    def __str__(self):
        return self.nazwa


class TradycjaBCS(models.Model):

    class Origins(models.TextChoices):
        ZAPOZYCZONA = "Z", "Zapożyczona"
        AUTORSKA = "A", "Autorka"

    class PewnoscStazu(models.TextChoices):
        TAK = "T", "Na pewno wcześniej się nie pojawiała"
        NIE = "N", "Ale mogła pojawić się wcześniej"

    nazwa = models.CharField(max_length=MEDIUM_LENGTH, verbose_name="Tradycja")

    zapozyczona_czy_autorska = models.CharField(
        choices=Origins.choices,
        blank=True,
        null=True,
        verbose_name="Zapożyczona czy autorska",
    )

    autor = models.ForeignKey(
        "osoby.Osoba",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Autor tradycji",
    )

    od_kogo = models.ForeignKey(
        "encyklopedia.GrupaBractw",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Od kogo zapożyczona",
    )

    okolicznosci_powstania = models.CharField(
        max_length=Lengths.OKOLICZNOSCI_LENGTH,
        choices=Okolicznosci.choices,
        blank=True,
        null=True,
        verbose_name="Okoliczności powstania",
    )

    wydarzenie = models.ForeignKey(
        Wydarzenie,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Wydarzenie",
        related_name="tradycje_zapoczatkowane_wydarzeniem",
    )

    inne = models.CharField(
        max_length=MAX_LENGTH,
        blank=True,
        verbose_name="Inna okoliczność (" "wpisz):",
    )

    pewnosc_stazu = models.CharField(
        choices=PewnoscStazu.choices,
        blank=True,
        null=True,
        verbose_name="Pewność czasu pojawienia się",
    )

    opis = models.TextField(blank=True, verbose_name="Opis")

    class Meta:
        verbose_name = "Tradycja BCS"
        verbose_name_plural = "Tradycje BCS"
        ordering = ("nazwa",)

    def __str__(self):
        autorska = (
            " - Autorska"
            if self.zapozyczona_czy_autorska == TradycjaBCS.Origins.AUTORSKA
            else ""
        )
        kontekst = ", "
        if (
            self.okolicznosci_powstania == Okolicznosci.WYDARZENIE
            and self.wydarzenie
        ):
            kontekst += str(self.wydarzenie)
        elif self.okolicznosci_powstania == Okolicznosci.INNE and self.inne:
            kontekst += str(self.inne)
        else:
            kontekst = ""
        return f"{self.nazwa}{autorska}{kontekst}"


class TradycjaInnegoBractwa(models.Model):

    nazwa = models.CharField(max_length=MEDIUM_LENGTH, verbose_name="Tradycja")

    bractwo = models.ForeignKey(
        Bractwo,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Bractwo",
    )

    zapozyczona = models.BooleanField(
        default=False, verbose_name="Zapożyczona"
    )

    od_kogo = models.ForeignKey(
        "encyklopedia.GrupaBractw",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Od kogo zapożyczona",
    )

    opis = models.TextField(blank=True, verbose_name="Opis")

    class Meta:
        verbose_name = "Tradycja innego bractwa"
        verbose_name_plural = "Tradycje innych bractw"
        ordering = ("nazwa",)

    def __str__(self):
        return self.nazwa


class Zwyczaj(models.Model):
    nazwa = models.CharField(max_length=MEDIUM_LENGTH, verbose_name="Nazwa")

    autor = models.ForeignKey(
        "osoby.Osoba",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Osoba, która zapoczątkowała zwyczaj",
    )

    data_powstania = models.DateField(
        blank=True, verbose_name="Data powstania"
    )

    opis = models.TextField(blank=True, verbose_name="Opis")

    class Meta:
        verbose_name = "Zwyczaj"
        verbose_name_plural = "Zwyczaje"
        ordering = ("nazwa",)

    def __str__(self):
        return self.nazwa
