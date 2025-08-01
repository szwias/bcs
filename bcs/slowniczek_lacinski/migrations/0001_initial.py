# Generated by Django 5.2.1 on 2025-07-24 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Zwrot",
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
                    "zwrot",
                    models.CharField(max_length=255, verbose_name="Zwrot"),
                ),
                (
                    "tlumaczenie",
                    models.CharField(
                        max_length=255, verbose_name="Tłumaczenie"
                    ),
                ),
                (
                    "uzywany_na_karczmie",
                    models.BooleanField(
                        default=False, verbose_name="Używany na Karczmie"
                    ),
                ),
            ],
            options={
                "verbose_name": "Zwrot",
                "verbose_name_plural": "Zwroty",
                "ordering": ["zwrot"],
            },
        ),
    ]
