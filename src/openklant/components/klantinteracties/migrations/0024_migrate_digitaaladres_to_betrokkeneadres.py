# Generated by Django 4.2.15 on 2024-11-08 11:53

from django.db import migrations


def migrate_digitaaladres_to_betrokkeneadres(apps, schema_editor):
    DigitaalAdres = apps.get_model("klantinteracties", "DigitaalAdres")
    BetrokkeneAdres = apps.get_model("klantinteracties", "BetrokkeneAdres")

    to_create = []
    for digitaal_adres in DigitaalAdres.objects.filter(betrokkene__isnull=False):
        to_create.append(
            BetrokkeneAdres(
                uuid=digitaal_adres.uuid,
                betrokkene=digitaal_adres.betrokkene,
                soort_digitaal_adres=digitaal_adres.soort_digitaal_adres,
                adres=digitaal_adres.adres,
                omschrijving=digitaal_adres.omschrijving,
            )
        )
        digitaal_adres.delete()

    if to_create:
        BetrokkeneAdres.objects.bulk_create(to_create)


def migrate_betrokkeneadres_to__digitaaladres(apps, schema_editor):
    DigitaalAdres = apps.get_model("klantinteracties", "DigitaalAdres")
    BetrokkeneAdres = apps.get_model("klantinteracties", "BetrokkeneAdres")

    to_create = []
    for betrokkene_adres in BetrokkeneAdres.objects.all():
        to_create.append(
            DigitaalAdres(
                uuid=betrokkene_adres.uuid,
                betrokkene=betrokkene_adres.betrokkene,
                soort_digitaal_adres=betrokkene_adres.soort_digitaal_adres,
                adres=betrokkene_adres.adres,
                omschrijving=betrokkene_adres.omschrijving,
            )
        )
        betrokkene_adres.delete()

    if to_create:
        DigitaalAdres.objects.bulk_create(to_create)


class Migration(migrations.Migration):

    dependencies = [
        ("klantinteracties", "0023_betrokkeneadres"),
    ]

    operations = [
        migrations.RunPython(
            migrate_digitaaladres_to_betrokkeneadres,
            migrate_betrokkeneadres_to__digitaaladres,
        )
    ]
