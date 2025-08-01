from django.db import models

from core.utils.Consts import MAX_LENGTH


class Zwrot(models.Model):

    zwrot = models.TextField(
        max_length=MAX_LENGTH, blank=True, null=True, verbose_name="Zwrot"
    )

    tlumaczenie = models.TextField(
        max_length=MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name="Tłumaczenie"
    )

    uzywany_na_karczmie = models.BooleanField(
        default=False, verbose_name="Używany na Karczmie"
    )

    class Meta:
        verbose_name = "Zwrot"
        verbose_name_plural = "Zwroty"
        ordering = ["zwrot"]

    def __str__(self):
        karczma = " (KARCZMA)" if self.uzywany_na_karczmie else ""
        return f"{self.zwrot} - {self.tlumaczenie}{karczma}"
