from django.utils import timezone

from core.utils.Choices import IntAlt
from core.utils.Czas import LATA_BRACTW
from core.utils.Lengths import MAX_LENGTH
from wyszukiwarka.models import SearchableModel
from wyszukiwarka.utils.Search import *


class Odznaczenie(SearchableModel):
    nazwa = models.CharField(max_length=MAX_LENGTH, verbose_name="Nazwa")

    opis = models.TextField(blank=True, verbose_name="Opis")

    rok_powstania = models.IntegerField(
        choices=LATA_BRACTW + [IntAlt.DONT_KNOW],
        default=IntAlt.DONT_KNOW,
        verbose_name="Rok powstania",
    )

    dokument = models.ForeignKey(
        to="zrodla.Dokument",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Dokument",
    )

    zarzad_funduje = models.BooleanField(
        default=False,
        verbose_name="Zarząd funduje",
    )

    fundatorzy = models.ManyToManyField(
        "osoby.Byt",
        blank=True,
        verbose_name="Fundatorzy",
    )

    class Meta:
        verbose_name = "Odznaczenie"
        verbose_name_plural = "Odznaczenia"
        ordering = ["nazwa"]

    def __str__(self):
        return self.nazwa


class Nagrodzeni(SearchableModel):
    data = models.DateField(
        default=timezone.now,
        blank=True,
        verbose_name="Data wręczenia odznaczenia",
    )

    odznaczenie = models.ForeignKey(
        to=Odznaczenie,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Odznaczenie",
    )

    osoba = models.ForeignKey(
        to="osoby.Byt",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Osoba/organizacja",
    )

    zaslugi = models.TextField(
        blank=True,
        verbose_name="Zasługi",
    )

    class Meta:
        verbose_name = "Nagrodzeni"
        verbose_name_plural = "Nagrodzeni"
        ordering = ["-data", "osoba"]

    def __str__(self):
        return f"{self.data} - {str(self.osoba)}"
