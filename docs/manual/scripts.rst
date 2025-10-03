
.. _scripts:

Scripts
=======

Dump data
---------

The ``dump_data.sh`` script can be used to export data from all components (**klantinteracties**, **contactgegevens**) to an SQL file.

This script is not intended for data migration to another Open Klant instance.

By default, the complete schema and data are generated in two SQL files. This can be adjusted using the flags ``--data-only``, ``--schema-only`` & ``--combined``,
which generate a single file. By default, the data dump contains all **klantinteractie** & **contactgegevens** data.

To export only specific data, the desired component names can be specified:

.. code-block:: shell

    ./dump_data.sh klantinteracties

.. note::

    To export a Postgres 17 database, the postgres-client-17 package is required.

Environment variabelen
----------------------

- **DB_HOST** = db
- **DB_PORT** = 5432
- **DB_USER** = openklant
- **DB_NAME** = openklant
- **DB_PASSWORD** = ''
- **DUMP_FILE** = dump_$(date +'%Y-%m-%d_%H-%M-%S').sql

.. code-block:: shell

    DB_HOST=localhost DB_NAME=openklant ./bin/dump_data.sh
