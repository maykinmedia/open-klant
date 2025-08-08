.. _migration_user_docs:

=========
Migration
=========

Users of Open Klant version ``1.0.0`` willing to migrate to version ``2.4.0`` or higher
can make use of the ``migrate_to_v2`` management command. This command **only** migrates
``Klant`` instances from version ``1.0.0``. The command expects two URLs; a URL for the
Open Klant instance of version ``1.0.0`` and a URL for version ``2.0.0``.

The command also expects environment variables for ``CLIENT_ID`` + ``SECRET`` OR ``ACCESS_TOKEN``
to be set, to authenticate to the Open Klant ``1.0.0`` instance. If all three are passed as
environment variables, the ``CLIENT_ID`` and ``SECRET`` are used instead of the ``ACCESS_TOKEN``.
For the ``2.0.0`` instance a dummy token will be created. This dummy token will be
removed after the command ran (be it successfully or not).

Examples of how one might want to run this command can be seen below:

    .. code-block:: bash

        $ CLIENT_ID="openklant-v1-client-id" SECRET="openklant-v1-secret" ./src/manage.py migrate_to_v2 \
            https://example.openklant.nl \
            https://example.klantinteracties.nl

Specifying the ``ACCESS_TOKEN`` directly:

    .. code-block:: bash

        $ ACCESS_TOKEN="openklant-v1-token" ./src/manage.py migrate_to_v2 \
            https://example.openklant.nl \
            https://example.klantinteracties.nl

When running the application in a Docker container:

    .. code-block:: bash

        $ docker exec -e CLIENT_ID="openklant-v1-client-id" -e SECRET="openklant-v1-secret" \
            <container_name> src/manage.py migrate_to_v2 \
            https://example.openklant.nl \
            https://example.klantinteracties.nl