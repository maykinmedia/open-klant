.. _migration_user_docs:

Migration
=========

Users of Open Klant version ``1.0.0`` willing to migrate to version ``2.4.0`` or higher
can make use of the ``migrate_to_v2`` management command. This command **only** migrates
``Klant`` instances from version ``1.0.0``. The command expects two URLs; a URL for the
Open Klant instance of version ``1.0.0`` and a URL for version ``2.0.0`` The command
also expects a ``ACCESS_TOKEN`` environment variable to be set, to authenticate to
the Open Klant ``1.0.0`` instance. For the ``2.0.0`` instance a dummy token will be
created. This dummy token will be removed after the command ran (be it successfully or not).
