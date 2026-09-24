
.. _scripts:

Scripts
=======

Dump data
---------

The ``dump_data.sh`` script can be used to export data from all components (**klantinteracties**, **contactgegevens**) to an SQL file or multiple CSV files.

This script is not intended for data migration to another Open Klant instance.

By default, the complete schema and data are generated in two SQL files. This can be adjusted using the flags ``--data-only``, ``--schema-only`` & ``--combined``,
which generate a single file. By default, the data dump contains all **klantinteractie** & **contactgegevens** data.

To export only specific data, the desired component names can be specified:

.. code-block:: shell

    /dump_data.sh klantinteracties

.. note::

    To export a Postgres 17 database, the postgres-client-17 package is required.

Adding the "--csv" flag exports all tables in the supplied components to CSV files. These files are temporarily placed in "csv_dumps" and combined into a TAR file.

Delete Klantcontacten not related to Zaken
-------------------------------------------

.. note::

    This script exists as a stopgap while `Open Archiefbeheer <https://open-archiefbeheer.readthedocs.io/en/stable/>`_
    does not yet support archiving/destroying Klantcontacten that have no Zaak relation.

The ``delete_klantcontacten_not_related_to_zaken`` management command is a temporary
cleanup script that deletes **Klantcontacten** that are not related to a **Zaak**,
along with everything that is removed as a result of that deletion and outputs a list of the deleted records.

A ``PartijIdentificator`` with a sub-identificator still pointing to it is normally
protected against deletion. If that sub-identificator is also being deleted here, the whole hierarchy is deleted
together. If a record that would be deleted is still protected by another record
outside of what is being deleted, the command aborts with a clear error
identifying the blocking records, without deleting anything. This also applies in
preview mode.

By default, only Klantcontacten with a ``plaatsgevondenOp`` date at least 12 months in
the past are eligible, and the command runs in **preview mode** (``--dry-run``, enabled
by default): it prints a destruction list ("vernietigingslijst") without deleting
anything. Pass ``--no-dry-run`` to actually delete the listed records.

.. code-block:: shell

    python src/manage.py delete_klantcontacten_not_related_to_zaken

Optionally, a date range can be specified with ``--minimum-date`` and/or
``--maximum-date`` (format ``YYYY-MM-DD``). ``--maximum-date`` must be at least 12
months in the past.

.. code-block:: shell

    python src/manage.py delete_klantcontacten_not_related_to_zaken \
        --minimum-date 2020-01-01 --maximum-date 2023-01-01

To actually delete the eligible records instead of only previewing them:

.. code-block:: shell

    python src/manage.py delete_klantcontacten_not_related_to_zaken --no-dry-run

.. note::

    Run this command inside the Docker container, e.g. via
    ``docker compose exec web python src/manage.py delete_klantcontacten_not_related_to_zaken``,
    when running Open Klant with Docker Compose.

Environment variabelen
----------------------

- **DB_HOST** = db
- **DB_PORT** = 5432
- **DB_USER** = openklant
- **DB_NAME** = openklant
- **DB_PASSWORD** = ''
- **DUMP_FILE** = dump_$(date +'%Y-%m-%d_%H-%M-%S').sql
- **TAR_FILE** ("dump_$(date +'%Y-%m-%d_%H-%M-%S').tar")

.. code-block:: shell

    DB_HOST=localhost DB_NAME=openklant ./bin/dump_data.sh
