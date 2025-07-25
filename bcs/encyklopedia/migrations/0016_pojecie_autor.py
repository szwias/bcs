# Generated by Django 5.2.1 on 2025-07-19 17:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("osoby", "0010_rename_bractwo_innaosoba_bractwo_do_ktorego_nalezy"),
        (
            "encyklopedia",
            "0015_remove_tradycjabcs_zapozyczona_tradycjabcs_autor_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="pojecie",
            name="autor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="osoby.osoba",
                verbose_name="Autor pojęcia",
            ),
        ),
    ]
