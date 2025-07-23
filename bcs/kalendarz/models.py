import os

from django.db import models
from django.utils import timezone

from core.utils.Consts import MAX_LENGTH, MEDIUM_LENGTH


# Create your models here.
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

    data = models.DateField(verbose_name="Data")

    godzina = models.TimeField(null=True, blank=True, verbose_name="Godzina")

    miejsce = models.ForeignKey(
        "miejsca.Miejsce",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Miejsce",
        related_name="zdarzenia_z_miejsca",
    )

    opis = models.TextField(blank=True, verbose_name="Opis")

    powiazane_osoby = models.ManyToManyField(
        "osoby.Osoba", blank=True, verbose_name="Powiązane osoby",
        db_table="kronika_zdarzenie_powiazane_osoby"
    )

    class Meta:
        db_table = "kronika_zdarzenie"
        verbose_name = "Zdarzenie"
        verbose_name_plural = "Zdarzenia"
        ordering = ["-data", "nazwa"]

    def __str__(self):
        godzina = str(self.godzina) + " " if self.godzina else ""
        wydarzenie_name = ""
        if self.wydarzenie:
            if (
                self.wydarzenie.typ_wydarzenia
                and not self.wydarzenie.typ_wydarzenia.is_sentinel()
            ):
                typ = str(self.wydarzenie.typ_wydarzenia)
            elif self.wydarzenie.typ_wyjazdu:
                typ = str(self.wydarzenie.typ_wyjazdu)
            else:
                typ = ""
            wydarzenie_name = f'{typ} "{self.wydarzenie.nazwa}"'

        return f"{self.data} {godzina}- {self.nazwa} ({wydarzenie_name})"

    def save(self, *args, **kwargs): # TODO: remove it, it's obsolete
        created = self._state.adding
        super().save(*args, **kwargs)

        if self.wydarzenie:
            if (
                self.wydarzenie.data_rozpoczecia
                == self.wydarzenie.data_zakonczenia
            ):
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
        max_length=MEDIUM_LENGTH, blank=True, verbose_name="Tytuł"
    )

    data = models.DateField(
        default=timezone.now, blank=True, verbose_name="Data wykonania"
    )

    miejsce = models.ForeignKey(
        "miejsca.Miejsce",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Miejsce",
        related_name="zdjecia_miejsca",
    )

    obraz = models.ImageField(
        upload_to="kronika/zdarzenia/", verbose_name="Dodaj obraz"
    )

    opis = models.TextField(blank=True, verbose_name="Opis")

    widoczne_osoby = models.ManyToManyField(
        "osoby.Osoba", blank=True, verbose_name="Widoczne osoby",
        db_table="kronika_obrazzdarzenie_widoczne_osoby"
    )

    class Meta:
        db_table = "kronika_obrazzdarzenie"
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
        max_length=MEDIUM_LENGTH, blank=True, verbose_name="Typ wydarzenia"
    )

    class Meta:
        db_table = "kronika_typwydarzenia"
        verbose_name = "Typ wydarzenia"
        verbose_name_plural = "Typy wydarzeń"
        ordering = ["typ"]

    def __str__(self):
        return self.typ

    def is_sentinel(self):
        return self.typ == "Nie dotyczy"

    @staticmethod
    def get_not_applicable_typ():
        return TypWydarzenia.objects.get(typ="Nie dotyczy")


class TypWyjazdu(models.Model):
    typ = models.CharField(
        max_length=MEDIUM_LENGTH,
        blank=True,
        verbose_name="Typ wyjazdu",
    )

    class Meta:
        db_table = "kronika_typwyjazdu"
        verbose_name = "Typ wyjazdu"
        verbose_name_plural = "Typy wyjazdów"
        ordering = ["typ"]

    def __str__(self):
        return self.typ

    def is_sentinel(self):
        return self.typ == "Nie dotyczy"

    @staticmethod
    def get_not_applicable_typ():
        return TypWyjazdu.objects.get(typ="Nie dotyczy")


class Wydarzenie(models.Model):

    nazwa = models.CharField(max_length=MAX_LENGTH, verbose_name="Nazwa")

    czy_jednodniowe = models.BooleanField(
        default=True, verbose_name="Jednodniowe"
    )

    data_rozpoczecia = models.DateField(
        default=timezone.now, verbose_name="Data rozpoczęcia"
    )

    data_zakonczenia = models.DateField(
        default=timezone.now, verbose_name="Data zakończenia"
    )

    miejsca = models.ManyToManyField(
        "miejsca.Miejsce", blank=True, verbose_name="Miejsca",
        db_table="kronika_wydarzenie_miejsca"
    )

    czy_to_wyjazd = models.BooleanField(
        default=False, verbose_name="Czy to wyjazd?"
    )

    typ_wydarzenia = models.ForeignKey(
        TypWydarzenia,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Typ wydarzenia",
    )

    typ_wyjazdu = models.ForeignKey(
        TypWyjazdu,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Typ wyjazdu",
    )

    link = models.URLField(blank=True, verbose_name="Link do wydarzenia na FB")

    opis = models.TextField(blank=True, verbose_name="Opis")

    uczestnicy = models.ManyToManyField(
        "osoby.Osoba", blank=True, verbose_name="Uczestnicy wydarzenia",
        db_table="kronika_wydarzenie_uczestnicy"
    )

    class Meta:
        db_table = "kronika_wydarzenie"
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"
        ordering = ["-data_rozpoczecia"]

    def __str__(self):
        name = f"{self.data_rozpoczecia}"
        if self.data_zakonczenia != self.data_rozpoczecia:
            name += f" - {self.data_zakonczenia}"

        if self.typ_wydarzenia and not self.typ_wydarzenia.is_sentinel():
            typ = str(self.typ_wydarzenia)
        elif self.typ_wyjazdu:
            typ = str(self.typ_wyjazdu)
        else:
            typ = ""

        if typ.lower() in self.nazwa.lower():
            typ = ""

        name += f': {typ} "{self.nazwa}"'
        return name


class ObrazWydarzenie(models.Model):
    wydarzenie = models.ForeignKey(
        Wydarzenie,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Wydarzenie",
        related_name="zdjecia_z_wydarzenia",
    )

    tytul = models.CharField(
        max_length=MEDIUM_LENGTH, blank=True, verbose_name="Tytuł"
    )

    obraz = models.ImageField(
        upload_to="kronika/wydarzenia/", verbose_name="Dodaj obraz"
    )

    opis = models.TextField(blank=True, verbose_name="Opis")

    widoczne_osoby = models.ManyToManyField(
        "osoby.Osoba", blank=True, verbose_name="Widoczne osoby",
        db_table="kronika_obrazwydarzenie_widoczne_osoby"
    )

    class Meta:
        db_table = "kronika_obrazwydarzenie"
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
