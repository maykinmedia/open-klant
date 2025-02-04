# Generated by Django 4.2.17 on 2025-02-04 15:44

import django.core.validators
from django.db import migrations, models
import openklant.utils.validators


class Migration(migrations.Migration):

    dependencies = [
        (
            "contactgegevens",
            "0005_alter_organisatie_adres_nummeraanduiding_id_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="organisatie",
            name="adres_huisnummer",
            field=models.IntegerField(
                blank=True,
                help_text="Huisnummer in het Basisregistratie Adressen en Gebouwen.",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(99999),
                ],
                verbose_name="huisnummer",
            ),
        ),
        migrations.AddField(
            model_name="organisatie",
            name="adres_huisnummertoevoeging",
            field=models.CharField(
                blank=True,
                help_text="Huisnummertoevoeging in het Basisregistratie Adressen en Gebouwen.",
                max_length=20,
                null=True,
                verbose_name="huisnummertoevoeging",
            ),
        ),
        migrations.AddField(
            model_name="organisatie",
            name="adres_postcode",
            field=models.CharField(
                blank=True,
                help_text="Postcode in het Basisregistratie Adressen en Gebouwen.",
                max_length=6,
                null=True,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Ongeldige postcode",
                        regex="^[1-9][0-9]{3} ?[a-zA-Z]{2}$",
                    )
                ],
                verbose_name="postcode",
            ),
        ),
        migrations.AddField(
            model_name="organisatie",
            name="adres_stad",
            field=models.CharField(
                blank=True,
                help_text="Stad in het Basisregistratie Adressen en Gebouwen.",
                max_length=255,
                null=True,
                verbose_name="stad",
            ),
        ),
        migrations.AddField(
            model_name="organisatie",
            name="adres_straatnaam",
            field=models.CharField(
                blank=True,
                help_text="Straatnaam in het Basisregistratie Adressen en Gebouwen.",
                max_length=255,
                null=True,
                verbose_name="straatnaam",
            ),
        ),
        migrations.AddField(
            model_name="persoon",
            name="adres_huisnummer",
            field=models.IntegerField(
                blank=True,
                help_text="Huisnummer in het Basisregistratie Adressen en Gebouwen.",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(99999),
                ],
                verbose_name="huisnummer",
            ),
        ),
        migrations.AddField(
            model_name="persoon",
            name="adres_huisnummertoevoeging",
            field=models.CharField(
                blank=True,
                help_text="Huisnummertoevoeging in het Basisregistratie Adressen en Gebouwen.",
                max_length=20,
                null=True,
                verbose_name="huisnummertoevoeging",
            ),
        ),
        migrations.AddField(
            model_name="persoon",
            name="adres_postcode",
            field=models.CharField(
                blank=True,
                help_text="Postcode in het Basisregistratie Adressen en Gebouwen.",
                max_length=6,
                null=True,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Ongeldige postcode",
                        regex="^[1-9][0-9]{3} ?[a-zA-Z]{2}$",
                    )
                ],
                verbose_name="postcode",
            ),
        ),
        migrations.AddField(
            model_name="persoon",
            name="adres_stad",
            field=models.CharField(
                blank=True,
                help_text="Stad in het Basisregistratie Adressen en Gebouwen.",
                max_length=255,
                null=True,
                verbose_name="stad",
            ),
        ),
        migrations.AddField(
            model_name="persoon",
            name="adres_straatnaam",
            field=models.CharField(
                blank=True,
                help_text="Straatnaam in het Basisregistratie Adressen en Gebouwen.",
                max_length=255,
                null=True,
                verbose_name="straatnaam",
            ),
        ),
    ]
