import os

from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from core.utils.Consts import MEDIUM_LENGTH


class Obraz(PolymorphicModel):
    tytul = models.CharField(max_length=MEDIUM_LENGTH, verbose_name="Tytuł")

    data = models.DateField(
        default=timezone.now, blank=True, verbose_name="Data wykonania"
    )

    opis = models.TextField(blank=True, verbose_name="Opis")


# Create your models here.
