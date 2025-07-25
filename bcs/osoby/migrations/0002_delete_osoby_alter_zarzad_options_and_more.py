# Generated by Django 5.2.1 on 2025-07-17 18:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
        ("osoby", "0001_initial"),
        ("encyklopedia", "0004_remove_powiedzenie_autor"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Osoby",
        ),
        migrations.AlterModelOptions(
            name="zarzad",
            options={
                "ordering": ["-kadencja"],
                "verbose_name": "Zarząd",
                "verbose_name_plural": "Zarządy",
            },
        ),
        migrations.AddField(
            model_name="dawnyzarzad",
            name="wielki_mistrz",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="kadencje_jako_wielki_mistrz_dawnego_zarzadu",
                to="osoby.wielkimistrz",
                verbose_name="Wielki Mistrz",
            ),
        ),
        migrations.AddField(
            model_name="innaosoba",
            name="bractwo",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="czlonkowie_bractwa",
                to="encyklopedia.bractwo",
                verbose_name="Bractwo",
            ),
        ),
        migrations.AddField(
            model_name="wielkimistrz",
            name="imie",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="osoby.czlonek",
                verbose_name="Imię",
            ),
        ),
        migrations.AddField(
            model_name="zarzad",
            name="cantandi",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="kadencje_jako_cantandi",
                to="osoby.czlonek",
                verbose_name="Cantandi",
            ),
        ),
        migrations.AddField(
            model_name="zarzad",
            name="kadencja",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.kadencja",
                verbose_name="Kadencja",
            ),
        ),
        migrations.AddField(
            model_name="zarzad",
            name="kasztelan",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="kadencje_jako_kasztelan",
                to="osoby.czlonek",
                verbose_name="Kasztelan",
            ),
        ),
        migrations.AddField(
            model_name="zarzad",
            name="sekretarz",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="kadencje_jako_sekretarz",
                to="osoby.czlonek",
                verbose_name="Sekretarz",
            ),
        ),
        migrations.AddField(
            model_name="zarzad",
            name="skarbnik",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="kadencje_jako_skarbnik",
                to="osoby.czlonek",
                verbose_name="Skarbnik",
            ),
        ),
        migrations.AddField(
            model_name="zarzad",
            name="wielki_mistrz",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="kadencje_jako_wielki_mistrz",
                to="osoby.wielkimistrz",
                verbose_name="Wielki Mistrz",
            ),
        ),
        migrations.AlterField(
            model_name="bean",
            name="rodzic_1",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="beani_pierwszy_wybor",
                to="osoby.czlonek",
                verbose_name="Rodzic czapkowy",
            ),
        ),
        migrations.AlterField(
            model_name="bean",
            name="rodzic_2",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="beani_drugi_wybor",
                to="osoby.czlonek",
                verbose_name="Drugi rodzic czapkowy",
            ),
        ),
    ]
