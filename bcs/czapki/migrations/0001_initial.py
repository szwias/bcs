# Generated by Django 5.2.1 on 2025-07-17 20:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("miejsca", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Czapka",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "kolor",
                    models.CharField(
                        default="", max_length=255, verbose_name="Kolor"
                    ),
                ),
                (
                    "uczelnia",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="miejsca.uczelnia",
                        verbose_name="Uczelnia",
                    ),
                ),
                (
                    "wydzial",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="miejsca.wydzial",
                        verbose_name="Wydział",
                    ),
                ),
            ],
            options={
                "verbose_name": "Czapka",
                "verbose_name_plural": "Czapki",
                "ordering": ["uczelnia", "kolor", "wydzial"],
            },
        ),
    ]
