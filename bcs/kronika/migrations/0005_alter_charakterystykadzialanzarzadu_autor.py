# Generated by Django 5.2.1 on 2025-07-19 12:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "osoby",
            "0008_remove_oldbean_czapka_1_remove_oldbean_czapka_2_and_more",
        ),
        ("kronika", "0004_alter_charakterystykadzialanzarzadu_autor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="charakterystykadzialanzarzadu",
            name="autor",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="osoby.czlonek",
                verbose_name="Autor",
            ),
        ),
    ]
