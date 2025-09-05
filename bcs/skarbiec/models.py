from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from djmoney.models.fields import MoneyField
from stdnum import iban  # biblioteka do walidacji IBAN
import datetime
from wyszukiwarka.utils.Search import *
from core.utils.Lengths import IBAN_LENGTH, MAX_LENGTH
from wyszukiwarka.models import SearchableModel

User = get_user_model()


class Konto(SearchableModel):
    wlasciciel = models.ForeignKey(
        "osoby.Byt",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Właściciel",
    )

    nazwa_alternatywna = models.CharField(
        max_length=MAX_LENGTH, blank=True, verbose_name="Nazwa alternatywna"
    )

    numer_konta = models.CharField(
        max_length=IBAN_LENGTH, blank=True, verbose_name="Numer konta"
    )

    adres = models.TextField(blank=True, verbose_name="Adres właściciela")

    opis = models.TextField(blank=True, verbose_name="Opis")

    @property
    def get_name(self):
        if self.wlasciciel:
            return str(self.wlasciciel)
        return self.nazwa_alternatywna

    class Meta:
        verbose_name = "Konto"
        verbose_name_plural = "Konta"
        ordering = ["wlasciciel", "nazwa_alternatywna"]

    def __str__(self):
        return self.get_name

    def clean(self):
        """Walidacja numeru konta: IBAN jeśli możliwe, albo zwykły numer."""
        if self.numer_konta:
            # jeśli numer wygląda jak IBAN
            if len(self.numer_konta) >= 15 and self.numer_konta[:2].isalpha():
                if not iban.is_valid(self.numer_konta):
                    raise ValidationError(
                        {"numer_konta": "Niepoprawny numer IBAN."}
                    )
            # inaczej traktujemy jako zwykły numer – brak dodatkowej walidacji


class Transakcja(SearchableModel):
    PRZYCHOD = "przychod"
    WYDATEK = "wydatek"
    TRANSACTION_TYPES = [(PRZYCHOD, "Przychód"), (WYDATEK, "Wydatek")]

    konto = models.ForeignKey(
        Konto,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Konto",
        related_name="transakcje_z_tego_konta",
    )

    tytul = models.TextField(verbose_name="Tytuł")

    typ = models.CharField(max_length=10, choices=TRANSACTION_TYPES)

    kwota = MoneyField(
        max_digits=14,
        blank=True,
        decimal_places=2,
        default_currency="PLN",
        verbose_name="Kwota (z kropką zamiast przecinka)",
    )

    data = models.DateField(
        default=datetime.date.today, verbose_name="Data zaksięgowania"
    )

    opis = models.TextField(blank=True, verbose_name="Opis")

    rozliczenie = models.ForeignKey(
        "zrodla.Rozliczenie",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Rozliczenie",
        related_name="rozliczane_transakcje",
    )

    dodal = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, verbose_name="Dodał/dodała"
    )

    @property
    def get_kwota(self):
        znak = "+" if self.typ == self.PRZYCHOD else "-"
        kwota = f"{self.kwota.amount} {self.kwota.currency}"
        return f"{znak}{kwota}"

    class Meta:
        verbose_name = "Transakcja"
        verbose_name_plural = "Transakcje"
        ordering = ["-data"]

    def __str__(self):
        typ = self.get_typ_display()
        return f"{self.data} {self.konto}: {typ} {self.get_kwota}"
