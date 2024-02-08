# Generated by Django 3.2.23 on 2024-02-08 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("klantinteracties", "0010_auto_20240207_1416"),
    ]

    operations = [
        migrations.RenameField(
            model_name="actor",
            old_name="objectidentificator_object_id",
            new_name="actoridentificator_object_id",
        ),
        migrations.RenameField(
            model_name="bijlage",
            old_name="objectidentificator_object_id",
            new_name="bijlageidentificator_object_id",
        ),
        migrations.RenameField(
            model_name="onderwerpobject",
            old_name="objectidentificator_object_id",
            new_name="onderwerpobjectidentificator_object_id",
        ),
        migrations.RemoveField(
            model_name="actor",
            name="objectidentificator_objecttype",
        ),
        migrations.RemoveField(
            model_name="actor",
            name="objectidentificator_register",
        ),
        migrations.RemoveField(
            model_name="actor",
            name="objectidentificator_soort_object_id",
        ),
        migrations.RemoveField(
            model_name="bijlage",
            name="objectidentificator_objecttype",
        ),
        migrations.RemoveField(
            model_name="bijlage",
            name="objectidentificator_register",
        ),
        migrations.RemoveField(
            model_name="bijlage",
            name="objectidentificator_soort_object_id",
        ),
        migrations.RemoveField(
            model_name="onderwerpobject",
            name="objectidentificator_objecttype",
        ),
        migrations.RemoveField(
            model_name="onderwerpobject",
            name="objectidentificator_register",
        ),
        migrations.RemoveField(
            model_name="onderwerpobject",
            name="objectidentificator_soort_object_id",
        ),
        migrations.AddField(
            model_name="actor",
            name="actoridentificator_code_objecttype",
            field=models.CharField(
                blank=True,
                help_text="Type van het object, bijvoorbeeld: 'INGESCHREVEN NATUURLIJK PERSOON'.",
                max_length=200,
                verbose_name="code objecttype",
            ),
        ),
        migrations.AddField(
            model_name="actor",
            name="actoridentificator_code_register",
            field=models.CharField(
                blank=True,
                help_text="Binnen het landschap van registers unieke omschrijving van het register waarin het object is geregistreerd, bijvoorbeeld: 'BRP'.",
                max_length=200,
                verbose_name="code register",
            ),
        ),
        migrations.AddField(
            model_name="actor",
            name="actoridentificator_code_soort_object_id",
            field=models.CharField(
                blank=True,
                help_text="Naam van de eigenschap die het object identificeert, bijvoorbeeld: 'Burgerservicenummer'.",
                max_length=200,
                verbose_name="code soort object ID",
            ),
        ),
        migrations.AddField(
            model_name="bijlage",
            name="bijlageidentificator_code_objecttype",
            field=models.CharField(
                blank=True,
                help_text="Type van het object, bijvoorbeeld: 'INGESCHREVEN NATUURLIJK PERSOON'.",
                max_length=200,
                verbose_name="code objecttype",
            ),
        ),
        migrations.AddField(
            model_name="bijlage",
            name="bijlageidentificator_code_register",
            field=models.CharField(
                blank=True,
                help_text="Binnen het landschap van registers unieke omschrijving van het register waarin het object is geregistreerd, bijvoorbeeld: 'BRP'.",
                max_length=200,
                verbose_name="code register",
            ),
        ),
        migrations.AddField(
            model_name="bijlage",
            name="bijlageidentificator_code_soort_object_id",
            field=models.CharField(
                blank=True,
                help_text="Naam van de eigenschap die het object identificeert, bijvoorbeeld: 'Burgerservicenummer'.",
                max_length=200,
                verbose_name="code soort object ID",
            ),
        ),
        migrations.AddField(
            model_name="onderwerpobject",
            name="onderwerpobjectidentificator_code_objecttype",
            field=models.CharField(
                blank=True,
                help_text="Type van het object, bijvoorbeeld: 'INGESCHREVEN NATUURLIJK PERSOON'.",
                max_length=200,
                verbose_name="code objecttype",
            ),
        ),
        migrations.AddField(
            model_name="onderwerpobject",
            name="onderwerpobjectidentificator_code_register",
            field=models.CharField(
                blank=True,
                help_text="Binnen het landschap van registers unieke omschrijving van het register waarin het object is geregistreerd, bijvoorbeeld: 'BRP'.",
                max_length=200,
                verbose_name="code register",
            ),
        ),
        migrations.AddField(
            model_name="onderwerpobject",
            name="onderwerpobjectidentificator_code_soort_object_id",
            field=models.CharField(
                blank=True,
                help_text="Naam van de eigenschap die het object identificeert, bijvoorbeeld: 'Burgerservicenummer'.",
                max_length=200,
                verbose_name="code soort object ID",
            ),
        ),
    ]
