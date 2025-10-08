import requests

from core.utils.Lengths import (
    MAX_LENGTH,
    SHORT_LENGTH,
    MEDIUM_LENGTH,
    EMOJI_LENGTH,
)
from wyszukiwarka.models import SearchableModel
from wyszukiwarka.utils.Search import *


class Kraj(SearchableModel):
    kraj = models.CharField(max_length=MEDIUM_LENGTH, verbose_name="Kraj")

    class Meta:
        verbose_name = "Kraj"
        verbose_name_plural = "Kraje"
        ordering = ["kraj"]

    def __str__(self):
        return self.kraj

    @staticmethod
    def get_polska():
        return Kraj.objects.get(kraj="Polska")


class Miejsce(SearchableModel):

    nazwa = models.CharField(max_length=MAX_LENGTH, verbose_name="Nazwa")

    adres = models.CharField(
        max_length=MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name="Adres (wystarczy skopiować z Googla i dodać kraj)",
    )

    niestandardowy_adres = models.CharField(
        max_length=MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name="Adres niestandardowy (niezrozumiały dla map)",
    )

    typ = models.ForeignKey(
        "miejsca.TypMiejsca",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Typ miejsca",
    )

    zamkniete_na_stale = models.BooleanField(
        default=False, verbose_name="Zamknięte na stałe"
    )

    latitude = models.FloatField(blank=True, null=True, editable=False)
    longitude = models.FloatField(blank=True, null=True, editable=False)

    class Meta:
        verbose_name = "Miejsce"
        verbose_name_plural = "Miejsca"
        ordering = ["nazwa"]

    def __str__(self):
        return f"{self.nazwa} - {str(self.typ)}, {self.adres}"

    def geocode_address(self):
        """
        Fill latitude and longitude from self.adres using Nominatim.
        """
        if not self.adres:
            return None

        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": self.adres, "format": "json", "limit": 1}
        response = requests.get(
            url=url,
            params=params,
            headers={"User-Agent": "django-miejsca-app"},
        )
        if response.status_code == 200 and response.json():
            result = response.json()[0]
            self.latitude = float(result["lat"])
            self.longitude = float(result["lon"])
            self.save()
            return self.latitude, self.longitude
        return None


class TypMiejsca(SearchableModel):

    nazwa = models.CharField(
        max_length=MEDIUM_LENGTH, verbose_name="Typ miejsca"
    )

    emoji = models.CharField(
        max_length=EMOJI_LENGTH,
        blank=True,
        null=True,
        verbose_name="Emoji",
    )

    class Meta:
        verbose_name = "Typ miejsca"
        verbose_name_plural = "Typy miejsc"
        ordering = ["nazwa"]

    def __str__(self):
        emoji = f"{self.emoji} " if self.emoji else ""
        return emoji + self.nazwa


class Uczelnia(SearchableModel):

    nazwa = models.CharField(max_length=MAX_LENGTH, verbose_name="Uczelnia")

    akronim = models.CharField(max_length=SHORT_LENGTH, verbose_name="Akronim")

    kraj = models.ForeignKey(
        to=Kraj,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Kraj",
    )

    class Meta:
        verbose_name = "Uczelnia"
        verbose_name_plural = "Uczelnie"
        ordering = ["kraj", "nazwa"]

    def __str__(self):
        return f"{self.nazwa} ({self.akronim})"

    @staticmethod
    def get_dont_know_uczelnia():
        uczelnia = Uczelnia.objects.get(
            nazwa="Nie wiem",
            akronim="XXX",
            kraj__kraj="Nie wiem",
        )
        return uczelnia

    @staticmethod
    def get_not_applicable_uczelnia():
        uczelnia = Uczelnia.objects.get(
            nazwa="Nie dotyczy",
            akronim="XXX",
            kraj__kraj="Nie dotyczy",
        )
        return uczelnia


class Wydzial(SearchableModel):

    nazwa = models.CharField(
        max_length=MAX_LENGTH, blank=True, verbose_name="Wydział"
    )

    skrot = models.CharField(
        max_length=SHORT_LENGTH, blank=True, verbose_name="Skrót"
    )

    uczelnia = models.ForeignKey(
        to=Uczelnia,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Uczelnia",
    )

    class Meta:
        verbose_name = "Wydział"
        verbose_name_plural = "Wydziały"
        ordering = ["uczelnia", "nazwa"]

    def __str__(self):
        return f"{str(self.uczelnia.akronim)}: {self.nazwa} ({self.skrot})"

    @staticmethod
    def get_dont_know_wydzial():
        wydzial = Wydzial.objects.get(
            nazwa="Nie wiem",
            skrot="XXX",
            uczelnia=Uczelnia.get_dont_know_uczelnia(),
        )
        return wydzial

    @staticmethod
    def get_not_applicable_wydzial():
        wydzial = Wydzial.objects.get(
            nazwa="Nie dotyczy",
            skrot="XXX",
            uczelnia=Uczelnia.get_not_applicable_uczelnia(),
        )
        return wydzial
