from django.db import models
from core.utils.Consts import MAX_LENGTH, SHORT_LENGTH, NAME_LENGTH, MEDIUM_LENGTH


class Kraj(models.Model):
    kraj = models.CharField(
        max_length=MEDIUM_LENGTH,
        verbose_name='Kraj',
    )

    class Meta:
        verbose_name = 'Kraj'
        verbose_name_plural = 'Kraje'
        ordering = ['kraj']

    def __str__(self):
        return self.kraj


class Uczelnia(models.Model): # TODO: add kraj (KrajCzapkowy)

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
