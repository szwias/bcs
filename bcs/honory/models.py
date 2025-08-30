from django.db import models

from core.utils.Choices import IntAlt
from core.utils.Consts import MAX_LENGTH
from core.utils.Czas import LATA_BRACTW


class Odznaczenie(models.Model):
    nazwa = models.CharField(max_length=MAX_LENGTH, verbose_name="Nazwa")

    opis = models.TextField(blank=True, verbose_name="Opis")

    rok_powstania = models.IntegerField(
        choices=LATA_BRACTW + [IntAlt.DONT_KNOW],
        default=IntAlt.DONT_KNOW,
        verbose_name="Rok powstania",
    )

    dokument = models.ForeignKey(
        "zrodla.Dokument",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Dokument",
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
