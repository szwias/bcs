from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from core.utils.Consts import MAX_LENGTH, MEDIUM_LENGTH


# Create your models here.
class Zdarzenie(models.Model):
    nazwa = models.CharField(max_length=MAX_LENGTH, verbose_name="Nazwa")

    wydarzenie = models.ForeignKey(
        "WydarzenieKalendarzowe",
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
        "osoby.Osoba",
        blank=True,
        verbose_name="Powiązane osoby",
    )

    class Meta:
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


class TypWydarzenia(models.Model):
    typ = models.CharField(
        max_length=MEDIUM_LENGTH, blank=True, verbose_name="Typ wydarzenia"
    )

    class Meta:
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


class WydarzenieKalendarzowe(PolymorphicModel):

    nazwa = models.CharField(max_length=MAX_LENGTH, verbose_name="Nazwa")

    data_rozpoczecia = models.DateField(
        default=timezone.now, verbose_name="Data rozpoczecia"
    )

    link = models.URLField(blank=True, verbose_name="Link do wydarzenia na FB")

    opis = models.TextField(blank=True, verbose_name="Opis")

    class Meta:
        verbose_name = "Wydarzenie kalendarzowe"
        verbose_name_plural = "Wydarzenia kalendarzowe"
        ordering = ["-data_rozpoczecia"]

    def __str__(self):
        return f"{self.data_rozpoczecia} - {self.nazwa}"

    pass


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
        "miejsca.Miejsce",
        blank=True,
        verbose_name="Miejsca",
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
        "osoby.Osoba",
        blank=True,
        verbose_name="Uczestnicy wydarzenia",
    )

    class Meta:
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


class WydarzenieDummy(WydarzenieKalendarzowe):

    czy_jednodniowe = models.BooleanField(
        default=True, verbose_name="Jednodniowe"
    )

    data_zakonczenia = models.DateField(
        default=timezone.now, verbose_name="Data zakończenia"
    )

    miejsca = models.ManyToManyField(
        "miejsca.Miejsce",
        blank=True,
        verbose_name="Miejsca",
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

    uczestnicy = models.ManyToManyField(
        "osoby.Osoba",
        blank=True,
        verbose_name="Uczestnicy wydarzenia",
    )

    class Meta:
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
