# Generated by Django 4.2.19 on 2025-03-11 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("klantinteracties", "0032_remove_internetaak_actoren_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="internetaak",
            old_name="new_actoren",
            new_name="actoren",
        ),
    ]
