# dashboard/models.py
from django.db import models
from django.urls import reverse, NoReverseMatch

from core.utils.Lengths import NAME_LENGTH, MEDIUM_LENGTH
from dashboard.utils import get_project_apps


class App(models.Model):
    aplikacja = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name="Aplikacja Django",
        choices=[(a, a) for a in get_project_apps()],
    )

    nazwa = models.CharField(
        max_length=MEDIUM_LENGTH,
        blank=True,
        null=True,
        verbose_name="Nazwa Aplikacji",
    )

    opis = models.CharField(
        max_length=MEDIUM_LENGTH,
        blank=True,
        null=True,
        verbose_name="Krótki opis",
    )

    ikona = models.CharField(
        blank=True,
        null=True,
        max_length=NAME_LENGTH,
        verbose_name="Ikona",
        help_text="Lokalizacja ikony w static/images/apps/ np. blog.svg",
    )

    adres_url = models.CharField(
        blank=True,
        null=True,
        max_length=NAME_LENGTH,
        verbose_name="Django URL",
        help_text="Adres URL głównego widoku aplikacji, np. 'blog:index'",
    )

    class Meta:
        ordering = ["nazwa", "aplikacja"]

    def __str__(self):
        return self.nazwa or self.aplikacja

    def get_absolute_url(self):
        try:
            return reverse(self.adres_url)
        except NoReverseMatch:
            return ""  # fallback URL

    def get_icon_static_path(self):
        return f"images/apps/{self.ikona}"
