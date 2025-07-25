# Generated by Django 5.2.1 on 2025-07-24 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kalendarz", "0002_alter_obrazwydarzenie_widoczne_osoby_and_more"),
        ("kronika", "0018_alter_wydarzeniehistoryczne_data_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="wydarzeniehistoryczne",
            name="wydarzenie",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="powiazane_wydarzenie_historyczne",
                to="kalendarz.wydarzenie",
                verbose_name="Powiązane wydarzenie z kalendarza",
            ),
        ),
    ]
