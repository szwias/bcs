from django.db import models

from core.utils.Consts import MAX_LENGTH


class Zwrot(models.Model):

    zwrot = models.CharField(max_length=MAX_LENGTH, verbose_name="Zwrot")

    tlumaczenie = models.CharField(
        max_length=MAX_LENGTH, verbose_name="Tłumaczenie"
    )

    uzywany_na_karczmie = models.BooleanField(
        default=False, verbose_name="Używany na Karczmie"
    )

    class Meta:
        verbose_name = "Zwrot"
        verbose_name_plural = "Zwroty"
        ordering = ["zwrot"]

    def __str__(self):
        return self.zwrot
