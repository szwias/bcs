import os

from django.db import models
from core.utils.Consts import *
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from czlonkowie.models import Czlonek, InnaOsoba


class Uczestnictwo(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    czlonek = models.ForeignKey(
        Czlonek,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Członek",
    )

    inna_osoba = models.ForeignKey(
        InnaOsoba,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Inna osoba",
    )

    class Meta:
        verbose_name = "Uczestnictwo"
        verbose_name_plural = "Uczestnictwo"

    def __str__(self):
        return f"{self.czlonek} - {self.content_type} - {self.content_object}"

class Miejsce(models.Model):
    class TypyMiejsc(models.TextChoices):
        INNY = "Inny", "Inny"
        OBIEKT_KULTURY = "ObKult", "Obiekt kultury"
        PUB = "Pub", "Pub/Klub"
        SZCZYT = "Szczyt", "Szczyt"
        UCZELNIA = "Uczel", "Uczelnia"

    nazwa = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="Nazwa",
    )

    adres = models.CharField(
        max_length=MAX_LENGTH,
        blank=True,
        default="Ulica 1, Kraków, Polska",
        verbose_name="Adres",
    )

    typ = models.CharField(
        max_length=SHORT_LENGTH,
        choices=TypyMiejsc.choices,
        verbose_name="Typ miejsca",
    )

    class Meta:
        verbose_name = "Miejsce"
        verbose_name_plural = "Miejsca"
        ordering = ["nazwa"]

    def __str__(self):
        return f"{self.nazwa} - {self.get_typ_display()}, {self.adres}"

class Zdarzenie(models.Model):
    nazwa = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="Nazwa",
    )

    data = models.DateField(
        default=timezone.now,
        verbose_name="Data",
    )

    opis = models.TextField(
        blank=True,
        verbose_name="Opis",
    )

    powiazane_osoby = GenericRelation(
        Uczestnictwo,
        blank=True,
        verbose_name="Powiązane osoby",
        related_query_name="uczestnictwo_w_zdarzeniu")

    class Meta:
        verbose_name = "Zdarzenie"
        verbose_name_plural = "Zdarzenia"
        ordering = ["-data", "nazwa"]

    def __str__(self):
        return f"{self.data.strftime('%Y.%d.%m')} - {self.nazwa}"


class Wydarzenie(models.Model):
    class TypyWydarzen(models.TextChoices):
        INNE = "I", "Inne"
        KARCZMA = "Karczma", "Karczma"
        KINO = "Kino", "Kino"
        KONFERENCJA_NAUKOWA = "KonfNauk", "Konferencja naukowa"
        GROBY = "Groby", "Groby"
        HISTORYCZNE = "H", "Historyczne"
        OGNISKO = "Ognisko", "Ognisko"
        OSTRY_DYZUR = "OD", "Ostry Dyżur"
        PLANSZOWKI = "Plansz", "Planszówki"
        REAKTYWACJA = "Reakty", "Reaktywacja"
        TEATR = "Teatr", "Teatr"
        WALNE = "Walne", "Walne"
        WYCIECZKA = "Wyc", "Wycieczka"
        WYBORY = "Wybory", "Wybory"
        ULANSKIE_ZDROWIE = "UZ", "Ułańskie Zdrowie"
        UROCZYSTOSC = "Urocz", "Uroczystość"
        ZAWODY_SPORTOWE = "ZS", "Zawody sportowe"

    nazwa = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="Nazwa"
    )

    data = models.DateField(
        default=timezone.now,
        verbose_name="Data",
    )

    miejsce = models.ForeignKey(
        Miejsce,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Miejsce",
    )

    typ = models.CharField(
        max_length=SHORT_LENGTH,
        choices=TypyWydarzen.choices,
        verbose_name="Typ wydarzenia",
    )

    obrazy = models.ManyToManyField(
        "ObrazWydarzenie",
        blank=True,
        verbose_name="Zdjęcia",
        related_name="wydarzenie_obraz",
    )

    opis = models.TextField(
        blank=True,
        verbose_name="Opis",
    )

    zdarzenia = models.ManyToManyField(
        Zdarzenie,
        blank=True,
        verbose_name="Zdarzenia",
    )

    uczestnicy = GenericRelation(
        Uczestnictwo,
        blank=True,
        verbose_name="Uczestnicy",
        related_query_name="uczestnictwo_w_wydarzeniu")

    class Meta:
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"
        ordering = ["-data"]

    def __str__(self):
        return f"{self.data.strftime('%Y.%d.%m')} - {self.nazwa}"

class ObrazWydarzenie(models.Model):
    wydarzenie = models.ForeignKey(
        Wydarzenie,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Wydarzenie",
    )

    tytul = models.CharField(
        max_length=MEDIUM_LENGTH,
        blank=True,
        verbose_name="Tytuł",
    )

    obraz = models.ImageField(
        upload_to="kronika/wydarzenia/",
        verbose_name="Dodaj obraz",
    )

    widoczni_czlonkowie = models.ForeignKey(
        Czlonek,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Widoczni członkowie",
    )

    inne_widoczne_osoby = models.ForeignKey(
        InnaOsoba,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Inne widoczne osoby",
    )

    opis = models.TextField(
        blank=True,
        verbose_name="Opis",
    )

    class Meta:
        verbose_name = "Zdjęcie z wydarzenia"
        verbose_name_plural = "Zdjęcia z wydarzeń"
        ordering = ["-wydarzenie"]

    def __str__(self):
        image_name = os.path.basename(self.obraz.name)
        name = f"{self.wydarzenie.nazwa} - "
        if self.tytul:
            name += self.tytul
        name += image_name
        return name


class Proces(models.Model):
    nazwa = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="Nazwa",
    )

    data_rozpoczecia = models.DateField(
        default=timezone.now,
        verbose_name="Data rozpoczęcia",
    )

    data_zakonczenia = models.DateField(
        default=timezone.now,
        verbose_name="Data zakończenia",
    )

    opis = models.TextField(
        blank=True,
        verbose_name="Opis",
    )

    zdarzenia = models.ManyToManyField(
        Zdarzenie,
        blank=True,
        verbose_name="Zdarzenia",
    )

    class Meta:
        verbose_name = "Proces"
        verbose_name_plural = "Procesy"
        ordering = ["-data_rozpoczecia"]

    def __str__(self):
        return f"{self.nazwa}: {self.data_rozpoczecia.strftime('%d.%m.%Y')} - {self.data_zakonczenia.strftime('%d.%m.%Y')}"

class Wyjazd(models.Model):
    class TypyWyjazdow(models.TextChoices):
        ADAPCIAK = "AD", "Adapciak"
        KUDLACZE = "KU", "Kudłacze"
        ZAGRANICZNE = "ZAGR", "Zagraniczny"

    nazwa = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="Nazwa",
    )

    data_rozpoczecia = models.DateField(
        default=timezone.now,
        verbose_name="Data rozpoczęcia",
    )

    data_zakonczenia = models.DateField(
        default=timezone.now,
        verbose_name="Data zakończenia",
    )

    typ = models.CharField(
        max_length=SHORT_LENGTH,
        choices=TypyWyjazdow.choices,
        verbose_name="Typ wyjazdu",
    )

    miejsce = models.ForeignKey(
        Miejsce,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Miejsce",
    )

    opis = models.TextField(
        blank=True,
        verbose_name="Opis",
    )

    zdarzenia = models.ManyToManyField(
        Zdarzenie,
        blank=True,
        verbose_name="Zdarzenia",
    )

    uczestnicy = GenericRelation(
        Uczestnictwo,
        blank=True,
        verbose_name="Uczestnicy",
        related_query_name="uczestnictwo_w_wyjezdzie")

    class Meta:
        verbose_name = "Wyjazd"
        verbose_name_plural = "Wyjazdy"
        ordering = ["-data_rozpoczecia"]

    def __str__(self):
        return f"{self.typ} \"{self.nazwa}\" - {self.miejsce}, {self.data_rozpoczecia.strftime('%d.%m.%Y')} - {self.data_zakonczenia.strftime('%d.%m.%Y')}"


