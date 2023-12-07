# Generated by Django 3.2.18 on 2023-12-07 10:37

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TokenAuth",
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
                ("token", models.CharField(max_length=40, verbose_name="token")),
                (
                    "contact_person",
                    models.CharField(
                        help_text="Name of the person in the organization who can access the API",
                        max_length=200,
                        verbose_name="contact person",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Email of the person, who can access the API",
                        max_length=254,
                        verbose_name="email",
                    ),
                ),
                (
                    "organization",
                    models.CharField(
                        blank=True,
                        help_text="Organization which has access to the API",
                        max_length=200,
                        verbose_name="organization",
                    ),
                ),
                (
                    "last_modified",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="Last date when the token was modified",
                        verbose_name="last modified",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="Date when the token was created",
                        verbose_name="created",
                    ),
                ),
                (
                    "application",
                    models.CharField(
                        blank=True,
                        help_text="Application which has access to the API",
                        max_length=200,
                        verbose_name="application",
                    ),
                ),
                (
                    "administration",
                    models.CharField(
                        blank=True,
                        help_text="Administration which has access to the API",
                        max_length=200,
                        verbose_name="administration",
                    ),
                ),
            ],
            options={
                "verbose_name": "token authorization",
                "verbose_name_plural": "token authorizations",
            },
        ),
    ]