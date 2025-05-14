import os

from django.db import models

from core.utils.Choices import TextChoose, TextAlt
from core.utils.Consts import *
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Miejsce(models.Model):
    class TypyMiejsc(models.TextChoices):
        INNY = "Inny", "Inny"
        MIASTO = "Miasto", "Miasto"
        OBIEKT_KULTURY = "ObKult", "Obiekt kultury"
        PUB = "Pub", "Pub/Klub"
        SZCZYT = "Szczyt", "Szczyt"
        UCZELNIA = "Uczel", "Uczelnia"

    nazwa = models.CharField(
        max_length=MAX_LENGTH, verbose_name="Nazwa",
    )

    adres = models.CharField(
        max_length=MAX_LENGTH,
        blank=True,
        default="Ulica 1, Kraków, Polska",
        verbose_name="Adres",
    )

    typ = models.CharField(
        max_length=SHORT_LENGTH, choices=TypyMiejsc.choices, verbose_name="Typ miejsca",
    )

    class Meta:
        verbose_name = "Miejsce"
        verbose_name_plural = "Miejsca"
        ordering = ["nazwa"]

    def __str__(self):
        return f"{self.nazwa} - {self.get_typ_display()}, {self.adres}"

class Zdarzenie(models.Model):
    nazwa = models.CharField(max_length=MAX_LENGTH, verbose_name="Nazwa")

    wydarzenie = models.ForeignKey(
        "Wydarzenie",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Wydarzenie",
        related_name="zdarzenia",  # key change here
    )

    data = models.DateField(
        default=timezone.now, verbose_name="Data"
    )

    miejsce = models.ForeignKey(
        Miejsce,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Miejsce",
    )

    opis = models.TextField(
        blank=True, verbose_name="Opis"
    )

    powiazane_osoby = GenericRelation(
        "czlonkowie.Osoby",
        blank=True,
        verbose_name="Powiązane osoby",
        related_query_name="uczestnictwo_w_zdarzeniu"
    )

    class Meta:
        verbose_name = "Zdarzenie"
        verbose_name_plural = "Zdarzenia"
        ordering = ["-data", "nazwa"]

    def __str__(self):
        return f"{self.data} - {self.nazwa}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if self.wydarzenie:
            if self.wydarzenie.data_rozpoczecia == self.wydarzenie.data_zakonczenia:
                self.data = self.wydarzenie.data_rozpoczecia
            if is_new:
                for osoba in self.wydarzenie.uczestnicy.all():
                    osoba.pk = None
                    osoba.content_object = self
                    osoba.save()

        super().save(*args, **kwargs)


class ObrazZdarzenie(models.Model):
    zdarzenie = models.ForeignKey(
        Zdarzenie,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Zdarzenie",
    )

    tytul = models.CharField(
        max_length=MEDIUM_LENGTH, blank=True, verbose_name="Tytuł",
    )

    data = models.DateField(
        default=timezone.now, blank=True, verbose_name="Data wykonania",
    )

    miejsce = models.ForeignKey(
        Miejsce,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Miejsce",
    )

    obraz = models.ImageField(
        upload_to="kronika/zdarzenia/", verbose_name="Dodaj obraz",
    )

    widoczne_osoby = GenericRelation(
        "czlonkowie.Osoby",
        blank=True,
        verbose_name="Widoczne osoby",
        related_query_name="widoczne_osoby"
    )

    opis = models.TextField(
        blank=True, verbose_name="Opis",
    )

    class Meta:
        verbose_name = "Zdjęcie ze zdarzenia"
        verbose_name_plural = "Zdjęcia ze zdarzeń"
        ordering = ["-data"]

    def __str__(self):
        image_name = os.path.basename(self.obraz.name)
        name = f"{self.zdarzenie.nazwa} - "
        if self.tytul:
            name += self.tytul
        else:
            name += image_name
        if self.data:
            name += f" {self.data}"
        return name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if self.zdarzenie:
            self.data = self.zdarzenie.data
            self.miejsce = self.zdarzenie.miejsce
            if is_new:
                for osoba in self.zdarzenie.powiazane_osoby.all():
                    osoba.pk = None
                    osoba.content_object = self
                    osoba.save()

        super().save(*args, **kwargs)

class Wydarzenie(models.Model):
    class TypyWydarzen(models.TextChoices):
        AKCJA = "Akcja", "Akcja"
        INNE = "Inne", "Inne"
        KARCZMA = "Karczma", "Karczma"
        KINO = "Kino", "Kino"
        KONFERENCJA_NAUKOWA = "KonfNauk", "Konferencja naukowa/wykład/prelekcja"
        GROBY = "Groby", "Groby"
        HISTORYCZNE = "Hist", "Historyczne"
        OGNISKO = "Ognisko", "Grill/Ognisko"
        OSTRY_DYZUR = "Ostry", "Ostry Dyżur"
        PLANSZOWKI = "Plansz", "Planszówki"
        REAKTYWACJA = "Reakty", "Reaktywacja"
        TEATR = "Teatr", "Teatr"
        WALNE = "Walne", "Walne"
        WYCIECZKA = "Wyciecz", "Wycieczka"
        WYBORY = "Wybory", "Wybory"
        ULANSKIE_ZDROWIE = "Ulanskie", "Ułańskie Zdrowie"
        UROCZYSTOSC = "Urocz", "Uroczystość"
        ZAWODY_SPORTOWE = "ZawodySp", "Zawody sportowe"

    class TypyWyjazdow(models.TextChoices):
        ADAPCIAK = "Adapciak", "Adapciak"
        INNY = "Inny", "Inny"
        KUDLACZE = "Kudlacze", "Kudłacze"
        ZAGRANICZNY = "ZAGR", "Zagraniczny"

    nazwa = models.CharField(
        max_length=MAX_LENGTH, verbose_name="Nazwa"
    )

    data_rozpoczecia = models.DateField(
        default=timezone.now, verbose_name="Data rozpoczęcia"
    )

    data_zakonczenia = models.DateField(
        default=timezone.now, verbose_name="Data zakończenia"
    )

    miejsca = models.ManyToManyField(
        Miejsce, blank=True, verbose_name="Miejsce"
    )

    czy_to_wyjazd = models.CharField(
        max_length=TextChoose.LENGTH,
        choices=TextChoose.choices(),
        default=TextChoose.NO[0],
        verbose_name="Czy to wyjazd?",
    )

    typ_wydarzenia = models.CharField(
        max_length=SHORT_LENGTH,
        choices=TypyWydarzen.choices + [TextAlt.NOT_APPLICABLE],
        default=TextAlt.NOT_APPLICABLE[0],
        verbose_name="Typ wydarzenia",
    )

    typ_wyjazdu = models.CharField(
        max_length=SHORT_LENGTH,
        choices=TypyWyjazdow.choices + [TextAlt.NOT_APPLICABLE],
        default=TextAlt.NOT_APPLICABLE[0],
        verbose_name="Typ wyjazdu",
    )

    obrazy = models.ManyToManyField(
        "ObrazWydarzenie",
        blank=True,
        verbose_name="Zdjęcia",
        related_name="wydarzenie_obraz",
    )

    opis = models.TextField(
        blank=True, verbose_name="Opis"
    )

    uczestnicy = GenericRelation(
        "czlonkowie.Osoby",
        blank=True,
        verbose_name="Uczestnicy",
        related_query_name="uczestnictwo_w_wydarzeniu"
    )

    class Meta:
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"
        ordering = ["-data_rozpoczecia"]

    def __str__(self):
        name = f"{self.data_rozpoczecia}"
        if self.data_zakonczenia != self.data_rozpoczecia:
            name += f" - {self.data_zakonczenia}"
        if self.get_typ_wydarzenia_display() != TextAlt.NOT_APPLICABLE[1]:
            typ = self.get_typ_wydarzenia_display()
        else:
            typ = self.get_typ_wyjazdu_display()
        name += f": {typ} \"{self.nazwa}\""
        return name

class ObrazWydarzenie(models.Model):
    wydarzenie = models.ForeignKey(
        Wydarzenie,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Wydarzenie",
    )

    tytul = models.CharField(
        max_length=MEDIUM_LENGTH, blank=True, verbose_name="Tytuł",
    )

    obraz = models.ImageField(
        upload_to="kronika/wydarzenia/", verbose_name="Dodaj obraz",
    )

    widoczne_osoby = GenericRelation(
        "czlonkowie.Osoby",
        blank=True,
        verbose_name="Widoczne osoby",
        related_query_name="widoczne_osoby"
    )

    opis = models.TextField(
        blank=True, verbose_name="Opis",
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
        else:
            name += image_name
        return name


class Proces(models.Model):
    nazwa = models.CharField(
        max_length=MAX_LENGTH, verbose_name="Nazwa",
    )

    data_rozpoczecia = models.DateField(
        default=timezone.now, verbose_name="Data rozpoczęcia",
    )

    data_zakonczenia = models.DateField(
        default=timezone.now, verbose_name="Data zakończenia",
    )

    opis = models.TextField(
        blank=True, verbose_name="Opis",
    )

    zdarzenia = models.ManyToManyField(
        Zdarzenie, blank=True, verbose_name="Zdarzenia",
    )

    class Meta:
        verbose_name = "Proces"
        verbose_name_plural = "Procesy"
        ordering = ["-data_rozpoczecia"]

    def __str__(self):
        return f"{self.nazwa}: {self.data_rozpoczecia} - {self.data_zakonczenia}"

