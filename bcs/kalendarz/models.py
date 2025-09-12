from django.utils import timezone
from polymorphic.models import PolymorphicModel

from wyszukiwarka.utils.Search import *
from core.utils.Lengths import MAX_LENGTH, MEDIUM_LENGTH
from wyszukiwarka.models import SearchableModel, SearchablePolymorphicModel


# Create your models here.
class Zdarzenie(SearchableModel):
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
        return f"{self.data} {godzina}- {self.nazwa}"


class TypWydarzenia(SearchableModel):
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


class TypWyjazdu(SearchableModel):
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


class WydarzenieKalendarzowe(SearchablePolymorphicModel):
    search_indexable = False

    nazwa = models.CharField(max_length=MAX_LENGTH, verbose_name="Nazwa")

    data_rozpoczecia = models.DateField(
        default=timezone.now, verbose_name="Data rozpoczecia"
    )

    link = models.URLField(
        blank=True, null=True, verbose_name="Link do wydarzenia na FB"
    )

    opis = models.TextField(blank=True, null=True, verbose_name="Opis")

    class Meta:
        verbose_name = "Wydarzenie kalendarzowe"
        verbose_name_plural = "Wydarzenia kalendarzowe"
        ordering = ["-data_rozpoczecia"]

    def __str__(self):
        return f"{self.data_rozpoczecia} - {self.nazwa}"


class Chrzest(WydarzenieKalendarzowe):
    search_indexable = True

    miejsce = models.ForeignKey(
        "miejsca.Miejsce",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Miejsce",
    )

    chrzczeni = models.ManyToManyField(
        "osoby.Czlonek",
        blank=True,
        verbose_name="Chrzczeni",
        related_name="chrzest_osoby",
    )

    hymn = models.ForeignKey(
        "spiewnik.Piosenka",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Odśpiewany przez beanów hymn",
    )

    dokument = models.ForeignKey(
        "zrodla.Dokument",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Dokument chrzcielny",
    )

    class Meta:
        verbose_name = "Chrzest"
        verbose_name_plural = "Chrzty"
        ordering = ["-data_rozpoczecia"]

    def __str__(self):
        chrzczeni = ", ".join(
            [f"{c.imie} {c.nazwisko}" for c in self.chrzczeni.all()]
        )
        return f'{self.data_rozpoczecia} "{self.nazwa}" - {chrzczeni}'


class Wydarzenie(WydarzenieKalendarzowe):
    search_indexable = True

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

        words = typ.lower().split()
        nazwa_lower = self.nazwa.lower()

        # check every contiguous subsequence of words
        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                seq = " ".join(words[i:j])
                if seq and seq in nazwa_lower:
                    typ = ""
                    break
            if typ == "":
                break

        name += f': {typ} "{self.nazwa}"'
        return name
