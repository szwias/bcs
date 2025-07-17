from django.db import models
from core.utils.Consts import MAX_LENGTH, MEDIUM_LENGTH
from miejsca.models import Wydzial


class Czapka(models.Model):

    wydzial = models.ForeignKey(
        'miejsca.Wydzial',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Wydział',
    )

    inny_powod = models.CharField(
        max_length=MEDIUM_LENGTH, blank=True, verbose_name='Inny powód koloru',
    )

    kolor = models.CharField(
        max_length=MAX_LENGTH, default='', verbose_name='Kolor',
    )

    class Meta:
        verbose_name = "Czapka"
        verbose_name_plural = "Czapki"
        ordering = ['wydzial', 'kolor']

    def __str__(self):
        if self.id == Czapka.get_dont_know_czapka().id:
            return "Nie wiem"
        if self.id == Czapka.get_not_applicable_czapka().id:
            return "Nie dotyczy"
        powod = self.inny_powod or f"{self.wydzial.uczelnia.akronim}_{self.wydzial.skrot}"
        return f"{powod}: {self.kolor}"

    @staticmethod
    def get_dont_know_czapka():
        czapka = Czapka.objects.get(
            wydzial=Wydzial.get_dont_know_wydzial(),
            kolor="Nie wiem"
        )
        return czapka

    @staticmethod
    def get_not_applicable_czapka():
        czapka = Czapka.objects.get(
            wydzial=Wydzial.get_not_applicable_wydzial(),
            kolor="Nie dotyczy"
        )
        return czapka
