# Generated by Django 4.2.19 on 2025-02-28 13:57

import django.core.validators
from django.db import migrations, models
import openklant.utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ("klantinteracties", "0028_partijidentificator_sub_identificator_van_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="betrokkene",
            name="bezoekadres_huisnummer",
            field=models.IntegerField(
                blank=True,
                help_text="Huisnummer van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(99999),
                ],
                verbose_name="huisnummer",
            ),
        ),
        migrations.AddField(
            model_name="betrokkene",
            name="bezoekadres_huisnummertoevoeging",
            field=models.CharField(
                blank=True,
                help_text="Huisnummertoevoeging van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=20,
                verbose_name="huisnummertoevoeging",
            ),
        ),
        migrations.AddField(
            model_name="betrokkene",
            name="bezoekadres_postcode",
            field=models.CharField(
                blank=True,
                help_text="Postcode van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=7,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Ongeldige postcode", regex="^[1-9][0-9]{3} [A-Z]{2}$"
                    )
                ],
                verbose_name="postcode",
            ),
        ),
        migrations.AddField(
            model_name="betrokkene",
            name="bezoekadres_stad",
            field=models.CharField(
                blank=True,
                help_text="Stad van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                verbose_name="stad",
            ),
        ),
        migrations.AddField(
            model_name="betrokkene",
            name="bezoekadres_straatnaam",
            field=models.CharField(
                blank=True,
                help_text="Straatnaam van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                verbose_name="straatnaam",
            ),
        ),
        migrations.AddField(
            model_name="betrokkene",
            name="correspondentieadres_huisnummer",
            field=models.IntegerField(
                blank=True,
                help_text="Huisnummer van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(99999),
                ],
                verbose_name="huisnummer",
            ),
        ),
        migrations.AddField(
            model_name="betrokkene",
            name="correspondentieadres_huisnummertoevoeging",
            field=models.CharField(
                blank=True,
                help_text="Huisnummertoevoeging van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=20,
                verbose_name="huisnummertoevoeging",
            ),
        ),
        migrations.AddField(
            model_name="betrokkene",
            name="correspondentieadres_postcode",
            field=models.CharField(
                blank=True,
                help_text="Postcode van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=7,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Ongeldige postcode", regex="^[1-9][0-9]{3} [A-Z]{2}$"
                    )
                ],
                verbose_name="postcode",
            ),
        ),
        migrations.AddField(
            model_name="betrokkene",
            name="correspondentieadres_stad",
            field=models.CharField(
                blank=True,
                help_text="Stad van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                verbose_name="stad",
            ),
        ),
        migrations.AddField(
            model_name="betrokkene",
            name="correspondentieadres_straatnaam",
            field=models.CharField(
                blank=True,
                help_text="Straatnaam van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                verbose_name="straatnaam",
            ),
        ),
        migrations.AddField(
            model_name="partij",
            name="bezoekadres_huisnummer",
            field=models.IntegerField(
                blank=True,
                help_text="Huisnummer van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(99999),
                ],
                verbose_name="huisnummer",
            ),
        ),
        migrations.AddField(
            model_name="partij",
            name="bezoekadres_huisnummertoevoeging",
            field=models.CharField(
                blank=True,
                help_text="Huisnummertoevoeging van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=20,
                verbose_name="huisnummertoevoeging",
            ),
        ),
        migrations.AddField(
            model_name="partij",
            name="bezoekadres_postcode",
            field=models.CharField(
                blank=True,
                help_text="Postcode van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=7,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Ongeldige postcode", regex="^[1-9][0-9]{3} [A-Z]{2}$"
                    )
                ],
                verbose_name="postcode",
            ),
        ),
        migrations.AddField(
            model_name="partij",
            name="bezoekadres_stad",
            field=models.CharField(
                blank=True,
                help_text="Stad van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                verbose_name="stad",
            ),
        ),
        migrations.AddField(
            model_name="partij",
            name="bezoekadres_straatnaam",
            field=models.CharField(
                blank=True,
                help_text="Straatnaam van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                verbose_name="straatnaam",
            ),
        ),
        migrations.AddField(
            model_name="partij",
            name="correspondentieadres_huisnummer",
            field=models.IntegerField(
                blank=True,
                help_text="Huisnummer van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(99999),
                ],
                verbose_name="huisnummer",
            ),
        ),
        migrations.AddField(
            model_name="partij",
            name="correspondentieadres_huisnummertoevoeging",
            field=models.CharField(
                blank=True,
                help_text="Huisnummertoevoeging van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=20,
                verbose_name="huisnummertoevoeging",
            ),
        ),
        migrations.AddField(
            model_name="partij",
            name="correspondentieadres_postcode",
            field=models.CharField(
                blank=True,
                help_text="Postcode van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=7,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Ongeldige postcode", regex="^[1-9][0-9]{3} [A-Z]{2}$"
                    )
                ],
                verbose_name="postcode",
            ),
        ),
        migrations.AddField(
            model_name="partij",
            name="correspondentieadres_stad",
            field=models.CharField(
                blank=True,
                help_text="Stad van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                verbose_name="stad",
            ),
        ),
        migrations.AddField(
            model_name="partij",
            name="correspondentieadres_straatnaam",
            field=models.CharField(
                blank=True,
                help_text="Straatnaam van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                verbose_name="straatnaam",
            ),
        ),
    ]
