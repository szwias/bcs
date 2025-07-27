from django.db import models
from polymorphic.models import PolymorphicModel

from core.utils.Consts import MAX_LENGTH, NAME_LENGTH


class Podmiot(PolymorphicModel):
    nazwa = models.CharField(max_length=NAME_LENGTH, verbose_name="Nazwa")

    aktualne = models.BooleanField(default=True, verbose_name="Aktualne")

    class Meta:
        verbose_name = "Podmiot"
        verbose_name_plural = "Podmioty"
        ordering = ["nazwa"]

    def __str__(self):
        aktualnosc = "" if self.aktualne else " - NIEAKTUALNE"
        return f"{self.nazwa}{aktualnosc}"


class Rola(Podmiot):
    class Meta:
        verbose_name = "Rola jednostki w Bractwie"
        verbose_name_plural = "Role jednostki w Bractwie"
        ordering = ["nazwa"]


class Struktura(Podmiot):
    class Meta:
        verbose_name = "Struktura w Bractwie"
        verbose_name_plural = "Struktury w Bractwie"
        ordering = ["nazwa"]


class RelacjaPrawna(models.Model):
    class Wybory(models.TextChoices):
        PRAWO = "P", "Prawo"
        OBOWIAZEK = "O", "Obowiązek"

    tresc = models.TextField(max_length=MAX_LENGTH, verbose_name="Treść")

    podmiot = models.ManyToManyField(
        Podmiot, blank=True, verbose_name="Podmiot"
    )

    prawo_czy_obowiazek = models.CharField(
        max_length=1, choices=Wybory.choices, verbose_name="Rodzaj relacji"
    )

    przedawnione = models.BooleanField(
        default=False, verbose_name="Przedawnione"
    )

    dokument = models.ForeignKey(
        "zrodla.Dokument",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Dokument",
    )

    class Meta:
        verbose_name = "Relacja prawna"
        verbose_name_plural = "Prawa i obowiązki"

    def __str__(self):
        przedawnione = " - PRZEDAWNIONE" if self.przedawnione else ""
        podmiot = ", ".join(str(p) for p in self.podmiot.all())
        return f"{podmiot}: {self.tresc}{przedawnione}"
