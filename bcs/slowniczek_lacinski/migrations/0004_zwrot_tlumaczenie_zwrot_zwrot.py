# Generated by Django 5.2.1 on 2025-07-28 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "slowniczek_lacinski",
            "0003_alter_zwrot_options_remove_zwrot_tlumaczenie_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="zwrot",
            name="tlumaczenie",
            field=models.TextField(
                blank=True, max_length=255, null=True, verbose_name="Tłumaczenie"
            ),
        ),
        migrations.AddField(
            model_name="zwrot",
            name="zwrot",
            field=models.TextField(
                blank=True, max_length=255, null=True, verbose_name="Zwrot"
            ),
        ),
    ]
