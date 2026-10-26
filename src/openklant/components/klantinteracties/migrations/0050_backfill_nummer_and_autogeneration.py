"""
Generate ``nummer`` of Klantcontact, Partij and InterneTaak at database level.

1. increase ``max_length`` to 12
2. create a sequence + trigger that generates an empty ``nummer``
3. backfill the records without ``nummer``
4. make ``nummer`` NOT NULL

Existing numbers are NOT changed (no zero padding): filters keep working with
the old values and padding can't create duplicates. New numbers have 12 digits.

Example, with existing records ``"0000000041"`` and ``"7"``:

* existing records keep ``"0000000041"`` and ``"7"``
* a record without ``nummer`` gets ``"000000000042"`` (after the highest number)
* a client value ``"500"`` is stored as ``"000000000500"`` and moves the
  sequence: the next generated ``nummer`` is ``"000000000501"``
* a lower client value (``"30"``) doesn't move the sequence back
* old formats are different strings: ``"0000000041"`` doesn't block
  ``"000000000041"`` when the sequence cycles back to it
"""

import re

from django.db import migrations
from django.db.models import CharField, Func, Q

import openklant.utils.fields

from ..utils import MAX_NUMMER, NUMMER_LENGTH

TABLES = (
    "klantinteracties_klantcontact",
    "klantinteracties_partij",
    "klantinteracties_internetaak",
)
MODELS = ("InterneTaak", "Klantcontact", "Partij")


def _schema_sql(table: str) -> tuple[str, str]:
    seq = f"{table}_nummer_seq"
    next_func = f"{table}_next_nummer"
    trg_func = f"{table}_set_nummer"
    trigger = f"{table}_set_nummer_trg"

    forward = f"""
    CREATE SEQUENCE IF NOT EXISTS {seq}
        MINVALUE 1 MAXVALUE {MAX_NUMMER} CYCLE;
    ALTER SEQUENCE {seq} MAXVALUE {MAX_NUMMER} CYCLE;

    -- initialise only a sequence that has never been used (idempotent)
    SELECT setval(
        '{seq}',
        LEAST(
            COALESCE(
                (SELECT MAX(nummer::bigint) FROM {table} WHERE nummer ~ '^[0-9]+$'),
                0
            ) + 1,
            {MAX_NUMMER}
        ),
        false
    )
    WHERE NOT (SELECT is_called FROM {seq});

    CREATE OR REPLACE FUNCTION {next_func}() RETURNS varchar AS $$
    DECLARE
        first_candidate bigint;
        candidate bigint;
        candidate_nummer varchar;
    BEGIN
        LOOP
            candidate := nextval('{seq}');

            IF first_candidate IS NULL THEN
                first_candidate := candidate;
            ELSIF candidate = first_candidate THEN
                RAISE EXCEPTION
                    'It was not possible to automatically generate the next number. '
                    'The maximum number of characters has been reached.'
                    USING ERRCODE = 'sequence_generator_limit_exceeded';
            END IF;

            candidate_nummer := lpad(candidate::text, {NUMMER_LENGTH}, '0');
            IF NOT EXISTS (SELECT 1 FROM {table} WHERE nummer = candidate_nummer) THEN
                RETURN candidate_nummer;
            END IF;
        END LOOP;
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE FUNCTION {trg_func}() RETURNS trigger AS $$
    BEGIN
        IF TG_OP = 'INSERT' THEN
            IF NEW.nummer IS NULL OR NEW.nummer = '' THEN
                NEW.nummer := {next_func}();
                RETURN NEW;
            END IF;
        ELSIF TG_OP = 'UPDATE' THEN
            IF NEW.nummer IS NULL OR NEW.nummer = '' THEN
                NEW.nummer := OLD.nummer;
                RETURN NEW;
            END IF;
            -- unchanged nummer: keep it as it is (old numbers aren't padded)
            IF NEW.nummer IS NOT DISTINCT FROM OLD.nummer THEN
                RETURN NEW;
            END IF;
        END IF;

        -- new or changed nummer supplied manually: zero pad it
        IF NEW.nummer ~ '^[0-9]+$' THEN
            NEW.nummer := lpad(NEW.nummer, {NUMMER_LENGTH}, '0');
        END IF;

        IF NEW.nummer ~ '^[0-9]+$' THEN
            PERFORM setval(
                '{seq}',
                GREATEST(NEW.nummer::bigint, (SELECT last_value FROM {seq})),
                true
            );
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    DROP TRIGGER IF EXISTS {trigger} ON {table};
    CREATE TRIGGER {trigger}
        BEFORE INSERT OR UPDATE ON {table}
        FOR EACH ROW EXECUTE FUNCTION {trg_func}();
    """

    reverse = f"""
    DROP TRIGGER IF EXISTS {trigger} ON {table};
    DROP FUNCTION IF EXISTS {trg_func}();
    DROP FUNCTION IF EXISTS {next_func}();
    DROP SEQUENCE IF EXISTS {seq};
    """
    return forward, reverse


def _backfill_nummer(apps, schema_editor):
    for model_name in MODELS:
        Model = apps.get_model("klantinteracties", model_name)
        Model.objects.filter(Q(nummer="") | Q(nummer__isnull=True)).update(
            nummer=Func(
                function=f"{Model._meta.db_table}_next_nummer",
                output_field=CharField(),
            )
        )


class Migration(migrations.Migration):
    dependencies = [
        ("klantinteracties", "0049_internetaken_actoren_verbose_name"),
    ]

    operations = [
        # 1. max_length 12 (still nullable)
        migrations.AlterField(
            model_name="internetaak",
            name="nummer",
            field=openklant.utils.fields.GeneratedCharField(
                blank=True,
                help_text="Uniek identificerend nummer dat tijdens communicatie tussen mensen kan worden gebruikt om de specifieke interne taak aan te duiden. Wordt automatisch gegenereerd als het niet wordt opgegeven. Let op: vanaf de volgende major release kan dit nummer niet meer door clients worden opgegeven en wordt het altijd automatisch gegenereerd. Gebruik ``referentienummer`` om een eigen nummer vast te leggen.",
                max_length=12,
                null=True,
                unique=True,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Het nummer moet uit 1 tot 12 cijfers bestaan.",
                        regex=re.compile("\\A[0-9]{1,12}\\Z"),
                    )
                ],
                verbose_name="nummer",
            ),
        ),
        migrations.AlterField(
            model_name="klantcontact",
            name="nummer",
            field=openklant.utils.fields.GeneratedCharField(
                blank=True,
                help_text="Uniek identificerend nummer dat tijdens communicatie tussen mensen kan worden gebruikt om het specifieke klantcontact aan te duiden. Wordt automatisch gegenereerd als het niet wordt opgegeven. Let op: vanaf de volgende major release kan dit nummer niet meer door clients worden opgegeven en wordt het altijd automatisch gegenereerd. Gebruik ``referentienummer`` om een eigen nummer vast te leggen.",
                max_length=12,
                null=True,
                unique=True,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Het nummer moet uit 1 tot 12 cijfers bestaan.",
                        regex=re.compile("\\A[0-9]{1,12}\\Z"),
                    )
                ],
                verbose_name="nummer",
            ),
        ),
        migrations.AlterField(
            model_name="partij",
            name="nummer",
            field=openklant.utils.fields.GeneratedCharField(
                blank=True,
                help_text="Uniek identificerend nummer dat tijdens communicatie tussen mensen kan worden gebruikt om de specifieke partij aan te duiden. Wordt automatisch gegenereerd als het niet wordt opgegeven. Let op: vanaf de volgende major release kan dit nummer niet meer door clients worden opgegeven en wordt het altijd automatisch gegenereerd. Gebruik ``referentienummer`` om een eigen nummer vast te leggen.",
                max_length=12,
                null=True,
                unique=True,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Het nummer moet uit 1 tot 12 cijfers bestaan.",
                        regex=re.compile("\\A[0-9]{1,12}\\Z"),
                    )
                ],
                verbose_name="nummer",
            ),
        ),
        # 2. sequence + generator function + trigger
        *[
            migrations.RunSQL(sql=forward, reverse_sql=reverse)
            for forward, reverse in map(_schema_sql, TABLES)
        ],
        # 3. backfill the records without nummer
        migrations.RunPython(
            _backfill_nummer,
            migrations.RunPython.noop,
            elidable=True,
        ),
        # 4. NOT NULL
        migrations.AlterField(
            model_name="internetaak",
            name="nummer",
            field=openklant.utils.fields.GeneratedCharField(
                blank=True,
                help_text="Uniek identificerend nummer dat tijdens communicatie tussen mensen kan worden gebruikt om de specifieke interne taak aan te duiden. Wordt automatisch gegenereerd als het niet wordt opgegeven. Let op: vanaf de volgende major release kan dit nummer niet meer door clients worden opgegeven en wordt het altijd automatisch gegenereerd. Gebruik ``referentienummer`` om een eigen nummer vast te leggen.",
                max_length=12,
                unique=True,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Het nummer moet uit 1 tot 12 cijfers bestaan.",
                        regex=re.compile("\\A[0-9]{1,12}\\Z"),
                    )
                ],
                verbose_name="nummer",
            ),
        ),
        migrations.AlterField(
            model_name="klantcontact",
            name="nummer",
            field=openklant.utils.fields.GeneratedCharField(
                blank=True,
                help_text="Uniek identificerend nummer dat tijdens communicatie tussen mensen kan worden gebruikt om het specifieke klantcontact aan te duiden. Wordt automatisch gegenereerd als het niet wordt opgegeven. Let op: vanaf de volgende major release kan dit nummer niet meer door clients worden opgegeven en wordt het altijd automatisch gegenereerd. Gebruik ``referentienummer`` om een eigen nummer vast te leggen.",
                max_length=12,
                unique=True,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Het nummer moet uit 1 tot 12 cijfers bestaan.",
                        regex=re.compile("\\A[0-9]{1,12}\\Z"),
                    )
                ],
                verbose_name="nummer",
            ),
        ),
        migrations.AlterField(
            model_name="partij",
            name="nummer",
            field=openklant.utils.fields.GeneratedCharField(
                blank=True,
                help_text="Uniek identificerend nummer dat tijdens communicatie tussen mensen kan worden gebruikt om de specifieke partij aan te duiden. Wordt automatisch gegenereerd als het niet wordt opgegeven. Let op: vanaf de volgende major release kan dit nummer niet meer door clients worden opgegeven en wordt het altijd automatisch gegenereerd. Gebruik ``referentienummer`` om een eigen nummer vast te leggen.",
                max_length=12,
                unique=True,
                validators=[
                    openklant.utils.validators.CustomRegexValidator(
                        message="Het nummer moet uit 1 tot 12 cijfers bestaan.",
                        regex=re.compile("\\A[0-9]{1,12}\\Z"),
                    )
                ],
                verbose_name="nummer",
            ),
        ),
    ]
