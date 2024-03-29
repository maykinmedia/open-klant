# Generated by Django 3.2.23 on 2024-01-26 12:04

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("klantinteracties", "0008_auto_20240116_1541"),
    ]

    operations = [
        migrations.CreateModel(
            name="Categorie",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        help_text="Unieke (technische) identificatiecode van de Categorie.",
                        unique=True,
                    ),
                ),
                (
                    "naam",
                    models.CharField(
                        blank=True,
                        help_text="Naam van de categorie.",
                        max_length=80,
                        verbose_name="naam",
                    ),
                ),
            ],
            options={
                "verbose_name": "categorie",
                "verbose_name_plural": "categorieën",
            },
        ),
        migrations.CreateModel(
            name="CategorieRelatie",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        help_text="Unieke (technische) identificatiecode van de Categorie Relatie.",
                        unique=True,
                    ),
                ),
                (
                    "begin_datum",
                    models.DateField(
                        blank=True,
                        help_text="Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. Een datum wordt genoteerd van het meest naar het minst significante onderdeel. Een voorbeeld: 2022-02-21",
                        null=True,
                        verbose_name="begin datum",
                    ),
                ),
                (
                    "eind_datum",
                    models.DateField(
                        blank=True,
                        help_text="Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. Een datum wordt genoteerd van het meest naar het minst significante onderdeel. Een voorbeeld: 2022-02-21",
                        null=True,
                        verbose_name="eind datum",
                    ),
                ),
                (
                    "categorie",
                    models.ForeignKey(
                        blank=True,
                        help_text="De 'categorie' van deze 'categorie relatie'.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="klantinteracties.categorie",
                        verbose_name="categorie",
                    ),
                ),
                (
                    "partij",
                    models.ForeignKey(
                        blank=True,
                        help_text="De 'categorie relatie' van een 'Partij'.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="klantinteracties.partij",
                        verbose_name="partij",
                    ),
                ),
            ],
            options={
                "verbose_name": "categorie relatie",
                "verbose_name_plural": "categorieën relatie",
            },
        ),
    ]
