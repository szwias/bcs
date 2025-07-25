# Generated by Django 5.2.1 on 2025-07-17 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Kadencja",
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
                    "rozpoczecie",
                    models.IntegerField(
                        choices=[
                            (2009, "2009"),
                            (2010, "2010"),
                            (2011, "2011"),
                            (2012, "2012"),
                            (2013, "2013"),
                            (2014, "2014"),
                            (2015, "2015"),
                            (2016, "2016"),
                            (2017, "2017"),
                            (2018, "2018"),
                            (2019, "2019"),
                            (2020, "2020"),
                            (2021, "2021"),
                            (2022, "2022"),
                            (2023, "2023"),
                            (2024, "2024"),
                            (2025, "2025"),
                        ],
                        verbose_name="Rozpoczęcie",
                    ),
                ),
                (
                    "zakonczenie",
                    models.IntegerField(
                        blank=True, verbose_name="Zakonczenie"
                    ),
                ),
            ],
            options={
                "verbose_name": "Kadencja",
                "verbose_name_plural": "Kadencje",
                "ordering": ["rozpoczecie"],
            },
        ),
    ]
