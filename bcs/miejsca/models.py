from django.db import models
from core.utils.Consts import MAX_LENGTH, SHORT_LENGTH, MEDIUM_LENGTH


class Kraj(models.Model):
    kraj = models.CharField(
        max_length=MEDIUM_LENGTH, verbose_name='Kraj',
    )

    class Meta:
        verbose_name = 'Kraj'
        verbose_name_plural = 'Kraje'
        ordering = ['kraj']

    def __str__(self):
        return self.kraj

    @staticmethod
    def get_polska():
        return Kraj.objects.get(kraj='Polska')


class Miejsce(models.Model):

    nazwa = models.CharField(
        max_length=MAX_LENGTH, verbose_name="Nazwa",
    )

    adres = models.CharField(
        max_length=MAX_LENGTH, blank=True, verbose_name="Adres",
    )

    typ = models.ForeignKey(
        "miejsca.TypMiejsca",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Typ miejsca",
    )

    zamkniete_na_stale = models.BooleanField(
        default=False, verbose_name="Zamknięte na stałe",
    )

    class Meta:
        verbose_name = "Miejsce"
        verbose_name_plural = "Miejsca"
        ordering = ["nazwa"]

    def __str__(self):
        return f"{self.nazwa} - {str(self.typ)}, {self.adres}"


class TypMiejsca(models.Model):

    nazwa = models.CharField(
        max_length=MEDIUM_LENGTH, verbose_name='Typ miejsca',
    )

    class Meta:
        verbose_name = 'Typ miejsca'
        verbose_name_plural = 'Typy miejsc'
        ordering = ['nazwa']

    def __str__(self):
        return self.nazwa


class Uczelnia(models.Model):

    nazwa = models.CharField(
        max_length=MAX_LENGTH, verbose_name="Uczelnia"
    )

    akronim = models.CharField(
        max_length=SHORT_LENGTH, verbose_name="Akronim"
    )

    kraj = models.ForeignKey(
        Kraj,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Kraj",
    )

    class Meta:
        verbose_name = "Uczelnia"
        verbose_name_plural = "Uczelnie"
        ordering = ['kraj', 'nazwa']

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

class Wydzial(models.Model):

    nazwa = models.CharField(
        max_length=MAX_LENGTH, blank=True, verbose_name="Wydział"
    )

    skrot = models.CharField(
        max_length=SHORT_LENGTH, blank=True, verbose_name="Skrót"
    )

    uczelnia = models.ForeignKey(
        Uczelnia,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Uczelnia",
    )

    class Meta:
        verbose_name = "Wydział"
        verbose_name_plural = "Wydziały"
        ordering = ['uczelnia', 'nazwa']

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
