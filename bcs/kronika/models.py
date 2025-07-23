from django.db import models


class CharakterystykaDzialanZarzadu(models.Model):
    zarzad = models.ForeignKey(
        "osoby.Zarzad",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Zarząd",
    )

    dawny_zarzad = models.ForeignKey(
        "osoby.DawnyZarzad",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Dawny Zarząd",
    )

    autor = models.ForeignKey(
        "osoby.Czlonek",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Autor",
    )

    charakterystyka = models.TextField(
        blank=True, verbose_name="Charakterystyka działań Zarządu"
    )

    class Meta:
        verbose_name = "Charakterystyka działań Zarządu"
        verbose_name_plural = "Charakterystyki działań Zarządów"
        ordering = ["-zarzad"]

    def __str__(self):
        return f"{self.autor}: {self.zarzad.kadencja if self.zarzad else self.dawny_zarzad.kadencja}"
