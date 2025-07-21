import os
from django.db import models

from core.utils.Choices import TextChoose, TextAlt
from core.utils.Consts import *
from django.utils import timezone


class Zdarzenie(models.Model):
    nazwa = models.CharField(max_length=MAX_LENGTH, verbose_name="Nazwa")

    wydarzenie = models.ForeignKey(
        "Wydarzenie",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Wydarzenie",
        related_name="zdarzenia_z_wydarzenia",
    )

    data = models.DateField(
        default=timezone.now, verbose_name="Data"
    )

    godzina = models.TimeField(
        null=True, blank=True, verbose_name="Godzina"
    )

    miejsce = models.ForeignKey(
        'miejsca.Miejsce',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Miejsce",
        related_name="zdarzenia_z_miejsca",
    )

    opis = models.TextField(
        blank=True, verbose_name="Opis"
    )

    powiazane_osoby = models.ManyToManyField(
        'osoby.Osoba', blank=True, verbose_name="Powiązane osoby"
    )

    class Meta:
        verbose_name = "Zdarzenie"
        verbose_name_plural = "Zdarzenia"
        ordering = ["-data", "nazwa"]

    def __str__(self):
        name = f"{self.data} {self.godzina} - {self.nazwa}"
        if self.wydarzenie:
            wydarzenie_name = ""
            if self.wydarzenie.get_typ_wydarzenia_display() != TextAlt.NOT_APPLICABLE[1]:
                typ = self.wydarzenie.get_typ_wydarzenia_display()
            else:
                typ = self.wydarzenie.get_typ_wyjazdu_display()
            wydarzenie_name += f"{typ} \"{self.wydarzenie.nazwa}\""
            name += f" ({wydarzenie_name})"

        return name

    def save(self, *args, **kwargs):
        created = self._state.adding
        super().save(*args, **kwargs)

        if self.wydarzenie:
            if self.wydarzenie.data_rozpoczecia == self.wydarzenie.data_zakonczenia:
                self.data = self.wydarzenie.data_rozpoczecia
            if created:
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
        related_name="zdjecia_ze_zdarzenia",
    )

    tytul = models.CharField(
        max_length=MEDIUM_LENGTH, blank=True, verbose_name="Tytuł",
    )

    data = models.DateField(
        default=timezone.now, blank=True, verbose_name="Data wykonania",
    )

    miejsce = models.ForeignKey(
        'miejsca.Miejsce',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Miejsce",
        related_name="zdjecia_miejsca",
    )

    obraz = models.ImageField(
        upload_to="kronika/zdarzenia/", verbose_name="Dodaj obraz",
    )

    opis = models.TextField(
        blank=True, verbose_name="Opis",
    )

    widoczne_osoby = models.ManyToManyField(
        'osoby.Osoba', blank=True, verbose_name="Widoczne osoby"
    )

    class Meta:
        verbose_name = "Zdjęcie ze zdarzenia"
        verbose_name_plural = "Zdjęcia ze zdarzeń"
        ordering = ["-data"]

    def __str__(self):
        image_name = os.path.basename(self.obraz.name)

        if self.zdarzenie:
            name = f"{self.zdarzenie.nazwa} - "
        else:
            name = ""

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


class TypWydarzenia(models.Model):
    typ = models.CharField(
        max_length=MEDIUM_LENGTH,
        blank=True,
        verbose_name="Typ wydarzenia",
    )

    class Meta:
        verbose_name = "Typ wydarzenia"
        verbose_name_plural = "Typy wydarzeń"
        ordering = ["typ"]

    def __str__(self):
        return self.typ


class TypWyjazdu(models.Model):
    typ = models.CharField(
        max_length=MEDIUM_LENGTH,
        blank=True,
        verbose_name="Typ wyjazdu",
    )

    class Meta:
        verbose_name = "Typ wyjazdu"
        verbose_name_plural = "Typy wyjazdów"
        ordering = ["typ"]

    def __str__(self):
        return self.typ


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
        ZAGRANICZNY = "ZAGR", "Wyjazd Zagraniczny"

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
        'miejsca.Miejsce', blank=True, verbose_name="Miejsca"
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

    link = models.URLField(
        blank=True, verbose_name="Link do wydarzenia na FB"
    )

    opis = models.TextField(
        blank=True, verbose_name="Opis"
    )

    uczestnicy = models.ManyToManyField(
        'osoby.Osoba', blank=True, verbose_name="Uczestnicy wydarzenia"
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
        related_name="zdjecia_z_wydarzenia"
    )

    tytul = models.CharField(
        max_length=MEDIUM_LENGTH, blank=True, verbose_name="Tytuł",
    )

    obraz = models.ImageField(
        upload_to="kronika/wydarzenia/", verbose_name="Dodaj obraz",
    )

    opis = models.TextField(
        blank=True, verbose_name="Opis",
    )

    widoczne_osoby = models.ManyToManyField(
        'osoby.Osoba', blank=True, verbose_name="Widoczne osoby"
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
        blank=True, verbose_name="Charakterystyka działań Zarządu",
    )

    class Meta:
        verbose_name = "Charakterystyka działań Zarządu"
        verbose_name_plural = "Charakterystyki działań Zarządów"
        ordering = ["-zarzad"]

    def __str__(self):
        return f"{self.autor}: {self.zarzad.kadencja if self.zarzad else self.dawny_zarzad.kadencja}"