from polymorphic.models import PolymorphicModel

from core.utils.Lengths import MAX_LENGTH, NAME_LENGTH
from wyszukiwarka.utils.Search import *
from wyszukiwarka.models import SearchableModel, SearchablePolymorphicModel


class DlugoscKadencji(SearchableModel):
    okres = models.CharField(
        max_length=MAX_LENGTH, verbose_name="Długość kadencji"
    )

    class Meta:
        verbose_name = "Długość kadencji"
        verbose_name_plural = "Długości kadencji"
        ordering = ["okres"]

    def __str__(self):
        return self.okres


class WielkoscStruktury(SearchableModel):
    wielkosc = models.CharField(max_length=MAX_LENGTH, verbose_name="Wielkość")

    class Meta:
        verbose_name = "Wielkość"
        verbose_name_plural = "Wielkości"
        ordering = ["wielkosc"]

    def __str__(self):
        return self.wielkosc


class Podmiot(SearchablePolymorphicModel):
    nazwa = models.CharField(max_length=NAME_LENGTH, verbose_name="Nazwa")

    dlugosc_kadencji = models.ForeignKey(
        to=DlugoscKadencji,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Długość kadencji",
    )

    aktualne = models.BooleanField(default=True, verbose_name="Aktualne")

    opis = models.TextField(blank=True, verbose_name="Opis")

    class Meta:
        verbose_name = "Podmiot"
        verbose_name_plural = "Podmioty"
        ordering = ["nazwa"]

    def __str__(self):
        return self.nazwa


class Rola(Podmiot):
    search_indexable = True

    class Meta:
        verbose_name = "Rola jednostki w Bractwie"
        verbose_name_plural = "Role jednostki w Bractwie"
        ordering = ["nazwa"]


class Struktura(Podmiot):
    search_indexable = True

    wielkosc = models.ForeignKey(
        to=WielkoscStruktury,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Wielkość",
    )

    class Meta:
        verbose_name = "Struktura w Bractwie"
        verbose_name_plural = "Struktury w Bractwie"
        ordering = ["nazwa"]


class RelacjaPrawna(SearchableModel):
    class Wybory(models.TextChoices):
        PRAWO = "P", "Prawo"
        OBOWIAZEK = "O", "Obowiązek"

    tresc = models.TextField(max_length=MAX_LENGTH, verbose_name="Treść")

    prawo_czy_obowiazek = models.CharField(
        max_length=1, choices=Wybory.choices, verbose_name="Rodzaj relacji"
    )

    class Meta:
        verbose_name = "Relacja prawna"
        verbose_name_plural = "Prawa i obowiązki"
        ordering = ["tresc"]

    def __str__(self):
        return self.tresc


class PrawoObowiazek(SearchableModel):
    podmiot = models.ForeignKey(
        to=Podmiot,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Podmiot",
    )

    relacja = models.ForeignKey(
        to=RelacjaPrawna,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Prawo/Obowiązek",
    )

    aktualne = models.BooleanField(default=True, verbose_name="Aktualne")

    dokument = models.ForeignKey(
        to="zrodla.Dokument",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Dokument",
    )

    class Meta:
        verbose_name = "Prawo/Obowiązek"
        verbose_name_plural = "Kodeks"
        ordering = ["podmiot", "relacja"]

    def __str__(self):
        aktualne = "" if self.aktualne else " - NIEAKTUALNE"
        return f"{self.podmiot}: {self.relacja}{aktualne}"
