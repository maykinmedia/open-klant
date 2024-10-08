# Generated by Django 4.2.11 on 2024-08-15 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("klantinteracties", "0017_auto_20240815_2234"),
    ]

    operations = [
        migrations.AlterField(
            model_name="internetaak",
            name="actor",
            field=models.ForeignKey(
                help_text="De actor aan wie de interne taak werd toegewezen.",
                on_delete=django.db.models.deletion.CASCADE,
                to="klantinteracties.actor",
                verbose_name="actor",
                default=1,
            ),
        ),
        migrations.RemoveField(
            model_name="internetaak",
            name="actor",
        ),
    ]
