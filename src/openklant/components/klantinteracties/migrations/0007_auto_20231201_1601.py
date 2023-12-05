# Generated by Django 3.2.18 on 2023-12-01 16:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("klantinteracties", "0006_auto_20231124_0956"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contactpersoon",
            name="organisatie",
        ),
        migrations.AddField(
            model_name="contactpersoon",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                help_text="Unieke (technische) identificatiecode van de contactpersoon.",
                unique=True,
            ),
        ),
        migrations.AddField(
            model_name="contactpersoon",
            name="werkte_voor_partij",
            field=models.ForeignKey(
                help_text="De organisatie waar een contactpersoon voor werkt.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="werkte_voor_partij",
                to="klantinteracties.partij",
                verbose_name="werkte voor partij",
            ),
        ),
        migrations.AlterField(
            model_name="contactpersoon",
            name="partij",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="klantinteracties.partij",
                verbose_name="partij",
            ),
        ),
        migrations.AlterField(
            model_name="geautomatiseerdeactor",
            name="actor",
            field=models.OneToOneField(
                help_text="'GeautomatiseerdeActor' was 'Actor'",
                on_delete=django.db.models.deletion.CASCADE,
                to="klantinteracties.actor",
                verbose_name="Actor",
            ),
        ),
        migrations.AlterField(
            model_name="medewerker",
            name="actor",
            field=models.OneToOneField(
                help_text="'GeautomatiseerdeActor' was 'Actor'",
                on_delete=django.db.models.deletion.CASCADE,
                to="klantinteracties.actor",
                verbose_name="actor",
            ),
        ),
        migrations.AlterField(
            model_name="organisatie",
            name="partij",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="klantinteracties.partij",
                verbose_name="partij",
            ),
        ),
        migrations.AlterField(
            model_name="organisatorischeeenheid",
            name="actor",
            field=models.OneToOneField(
                help_text="'GeautomatiseerdeActor' was 'Actor'",
                on_delete=django.db.models.deletion.CASCADE,
                to="klantinteracties.actor",
                verbose_name="actor",
            ),
        ),
        migrations.AlterField(
            model_name="persoon",
            name="partij",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="klantinteracties.partij",
                verbose_name="partij",
            ),
        ),
    ]
