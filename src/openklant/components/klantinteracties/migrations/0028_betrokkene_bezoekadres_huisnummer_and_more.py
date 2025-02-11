# Generated by Django 4.2.17 on 2025-02-11 13:52

import django.core.validators
from django.db import migrations, models
import openklant.utils.validators


def handle_null_values(apps, schema_editor):
    Betrokkene = apps.get_model("klantinteracties", "Betrokkene")
    Partij = apps.get_model("klantinteracties", "Partij")

    Betrokkene.objects.filter(
        bezoekadres_huisnummer__isnull=True,
        bezoekadres_huisnummertoevoeging__isnull=True,
        bezoekadres_postcode__isnull=True,
        bezoekadres_stad__isnull=True,
        bezoekadres_straatnaam__isnull=True,
        correspondentieadres_huisnummer__isnull=True,
        correspondentieadres_huisnummertoevoeging__isnull=True,
        correspondentieadres_postcode__isnull=True,
        correspondentieadres_stad__isnull=True,
        correspondentieadres_straatnaam__isnull=True,
    ).update(
        bezoekadres_huisnummer="",
        bezoekadres_huisnummertoevoeging="",
        bezoekadres_postcode="",
        bezoekadres_stad="",
        bezoekadres_straatnaam="",
        correspondentieadres_huisnummer="",
        correspondentieadres_huisnummertoevoeging="",
        correspondentieadres_postcode="",
        correspondentieadres_stad="",
        correspondentieadres_straatnaam="",
    )

    Partij.objects.filter(
        bezoekadres_huisnummer__isnull=True,
        bezoekadres_huisnummertoevoeging__isnull=True,
        bezoekadres_postcode__isnull=True,
        bezoekadres_stad__isnull=True,
        bezoekadres_straatnaam__isnull=True,
        correspondentieadres_huisnummer__isnull=True,
        correspondentieadres_huisnummertoevoeging__isnull=True,
        correspondentieadres_postcode__isnull=True,
        correspondentieadres_stad__isnull=True,
        correspondentieadres_straatnaam__isnull=True,
    ).update(
        bezoekadres_huisnummer="",
        bezoekadres_huisnummertoevoeging="",
        bezoekadres_postcode="",
        bezoekadres_stad="",
        bezoekadres_straatnaam="",
        correspondentieadres_huisnummer="",
        correspondentieadres_huisnummertoevoeging="",
        correspondentieadres_postcode="",
        correspondentieadres_stad="",
        correspondentieadres_straatnaam="",
    )


class Migration(migrations.Migration):

    dependencies = [
        (
            "klantinteracties",
            "0027_alter_betrokkene_bezoekadres_nummeraanduiding_id_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="betrokkene",
            name="bezoekadres_huisnummer",
            field=models.CharField(
                blank=True,
                help_text="Huisnummer van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                null=True,
                max_length=5,
                validators=[django.core.validators.validate_integer],
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
                null=True,
                verbose_name="huisnummertoevoeging",
            ),
        ),
        migrations.AddField(
            model_name="betrokkene",
            name="bezoekadres_postcode",
            field=models.CharField(
                blank=True,
                help_text="Postcode van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
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
            model_name="betrokkene",
            name="bezoekadres_stad",
            field=models.CharField(
                blank=True,
                help_text="Stad van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                null=True,
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
                null=True,
                verbose_name="straatnaam",
            ),
        ),
        migrations.AddField(
            model_name="betrokkene",
            name="correspondentieadres_huisnummer",
            field=models.CharField(
                blank=True,
                help_text="Huisnummer van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                null=True,
                max_length=5,
                validators=[django.core.validators.validate_integer],
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
                null=True,
                verbose_name="huisnummertoevoeging",
            ),
        ),
        migrations.AddField(
            model_name="betrokkene",
            name="correspondentieadres_postcode",
            field=models.CharField(
                blank=True,
                help_text="Postcode van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
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
            model_name="betrokkene",
            name="correspondentieadres_stad",
            field=models.CharField(
                blank=True,
                help_text="Stad van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                null=True,
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
                null=True,
                verbose_name="straatnaam",
            ),
        ),
        migrations.AddField(
            model_name="partij",
            name="bezoekadres_huisnummer",
            field=models.CharField(
                blank=True,
                help_text="Huisnummer van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                null=True,
                max_length=5,
                validators=[django.core.validators.validate_integer],
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
                null=True,
                verbose_name="huisnummertoevoeging",
            ),
        ),
        migrations.AddField(
            model_name="partij",
            name="bezoekadres_postcode",
            field=models.CharField(
                blank=True,
                help_text="Postcode van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
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
            model_name="partij",
            name="bezoekadres_stad",
            field=models.CharField(
                blank=True,
                help_text="Stad van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                null=True,
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
                null=True,
                verbose_name="straatnaam",
            ),
        ),
        migrations.AddField(
            model_name="partij",
            name="correspondentieadres_huisnummer",
            field=models.CharField(
                blank=True,
                help_text="Huisnummer van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                null=True,
                max_length=5,
                validators=[django.core.validators.validate_integer],
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
                null=True,
                verbose_name="huisnummertoevoeging",
            ),
        ),
        migrations.AddField(
            model_name="partij",
            name="correspondentieadres_postcode",
            field=models.CharField(
                blank=True,
                help_text="Postcode van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
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
            model_name="partij",
            name="correspondentieadres_stad",
            field=models.CharField(
                blank=True,
                help_text="Stad van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                null=True,
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
                null=True,
                verbose_name="straatnaam",
            ),
        ),
        migrations.RunPython(
            code=handle_null_values,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="betrokkene",
            name="bezoekadres_huisnummer",
            field=models.CharField(
                blank=True,
                help_text="Huisnummer van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=5,
                validators=[django.core.validators.validate_integer],
                verbose_name="huisnummer",
            ),
        ),
        migrations.AlterField(
            model_name="betrokkene",
            name="bezoekadres_huisnummertoevoeging",
            field=models.CharField(
                blank=True,
                help_text="Huisnummertoevoeging van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=20,
                verbose_name="huisnummertoevoeging",
            ),
        ),
        migrations.AlterField(
            model_name="betrokkene",
            name="bezoekadres_postcode",
            field=models.CharField(
                blank=True,
                help_text="Postcode van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=6,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Ongeldige postcode",
                        regex="^[1-9][0-9]{3} ?[a-zA-Z]{2}$",
                    )
                ],
                verbose_name="postcode",
            ),
        ),
        migrations.AlterField(
            model_name="betrokkene",
            name="bezoekadres_stad",
            field=models.CharField(
                blank=True,
                help_text="Stad van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                verbose_name="stad",
            ),
        ),
        migrations.AlterField(
            model_name="betrokkene",
            name="bezoekadres_straatnaam",
            field=models.CharField(
                blank=True,
                help_text="Straatnaam van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                verbose_name="straatnaam",
            ),
        ),
        migrations.AlterField(
            model_name="betrokkene",
            name="correspondentieadres_huisnummer",
            field=models.CharField(
                blank=True,
                help_text="Huisnummer van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=5,
                validators=[django.core.validators.validate_integer],
                verbose_name="huisnummer",
            ),
        ),
        migrations.AlterField(
            model_name="betrokkene",
            name="correspondentieadres_huisnummertoevoeging",
            field=models.CharField(
                blank=True,
                help_text="Huisnummertoevoeging van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=20,
                verbose_name="huisnummertoevoeging",
            ),
        ),
        migrations.AlterField(
            model_name="betrokkene",
            name="correspondentieadres_postcode",
            field=models.CharField(
                blank=True,
                help_text="Postcode van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=6,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Ongeldige postcode",
                        regex="^[1-9][0-9]{3} ?[a-zA-Z]{2}$",
                    )
                ],
                verbose_name="postcode",
            ),
        ),
        migrations.AlterField(
            model_name="betrokkene",
            name="correspondentieadres_stad",
            field=models.CharField(
                blank=True,
                help_text="Stad van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                verbose_name="stad",
            ),
        ),
        migrations.AlterField(
            model_name="betrokkene",
            name="correspondentieadres_straatnaam",
            field=models.CharField(
                blank=True,
                help_text="Straatnaam van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                verbose_name="straatnaam",
            ),
        ),
        migrations.AlterField(
            model_name="partij",
            name="bezoekadres_huisnummer",
            field=models.CharField(
                blank=True,
                help_text="Huisnummer van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=5,
                validators=[django.core.validators.validate_integer],
                verbose_name="huisnummer",
            ),
        ),
        migrations.AlterField(
            model_name="partij",
            name="bezoekadres_huisnummertoevoeging",
            field=models.CharField(
                blank=True,
                help_text="Huisnummertoevoeging van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=20,
                verbose_name="huisnummertoevoeging",
            ),
        ),
        migrations.AlterField(
            model_name="partij",
            name="bezoekadres_postcode",
            field=models.CharField(
                blank=True,
                help_text="Postcode van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=6,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Ongeldige postcode",
                        regex="^[1-9][0-9]{3} ?[a-zA-Z]{2}$",
                    )
                ],
                verbose_name="postcode",
            ),
        ),
        migrations.AlterField(
            model_name="partij",
            name="bezoekadres_stad",
            field=models.CharField(
                blank=True,
                help_text="Stad van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                verbose_name="stad",
            ),
        ),
        migrations.AlterField(
            model_name="partij",
            name="bezoekadres_straatnaam",
            field=models.CharField(
                blank=True,
                help_text="Straatnaam van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                verbose_name="straatnaam",
            ),
        ),
        migrations.AlterField(
            model_name="partij",
            name="correspondentieadres_huisnummer",
            field=models.CharField(
                blank=True,
                help_text="Huisnummer van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=5,
                validators=[django.core.validators.validate_integer],
                verbose_name="huisnummer",
            ),
        ),
        migrations.AlterField(
            model_name="partij",
            name="correspondentieadres_huisnummertoevoeging",
            field=models.CharField(
                blank=True,
                help_text="Huisnummertoevoeging van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=20,
                verbose_name="huisnummertoevoeging",
            ),
        ),
        migrations.AlterField(
            model_name="partij",
            name="correspondentieadres_postcode",
            field=models.CharField(
                blank=True,
                help_text="Postcode van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=6,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Ongeldige postcode",
                        regex="^[1-9][0-9]{3} ?[a-zA-Z]{2}$",
                    )
                ],
                verbose_name="postcode",
            ),
        ),
        migrations.AlterField(
            model_name="partij",
            name="correspondentieadres_stad",
            field=models.CharField(
                blank=True,
                help_text="Stad van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
                max_length=255,
                verbose_name="stad",
            ),
        ),
        migrations.AlterField(
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
