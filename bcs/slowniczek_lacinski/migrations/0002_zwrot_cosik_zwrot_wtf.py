# Generated by Django 5.2.1 on 2025-07-27 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("slowniczek_lacinski", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="zwrot",
            name="cosik",
            field=models.TextField(
                blank=True, max_length=255, null=True, verbose_name="Tłumaczenie"
            ),
        ),
        migrations.AddField(
            model_name="zwrot",
            name="wtf",
            field=models.TextField(
                blank=True, max_length=255, null=True, verbose_name="Zwrot"
            ),
        ),
    ]
