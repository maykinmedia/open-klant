.. _migration_developer_docs:

Migration
=========

To test the migration command, tests are written using VCR, which records the (relevant)
outgoing requests to cassette files. Whenever tests need to be updated, consider
re-recording the corresponding cassettes.

To re-record tests, a separate docker compose file is available to run a
version ``1.0.0`` Open Klant instance next to the ``StaticLiveServer`` (which
sets up a live server) which runs version ``2.0.0``. The `web` container from the
docker compose setup should load the corresponding fixture which reside in the
``migration/fixtures`` folder. A typical workflow, to re-record cassettes,
could look like the following:

.. code-block:: bash

    # Start the docker compose setup
    $ docker compose up --detach

    # Load a fixture for a certain test
    $ docker compose exec -it web \
        ./src/manage.py loaddata migration/credentials migration/test_digitaal_adres

    # Run the corresponding test
    $ ./src/manage.py test openklant.tests.test_migrate.MigrateTestCase.test_digitaal_adres

    # Stop and destroy the containers (to start with a clean slate on the next run)
    $ docker compose down


After running the test a cassette should be created (with the test name as filename)
in the ``migration/cassettes`` folder.

Note that the docker compose setup, with its fixtures are only needed to (re)create
cassettes for VCR. The migration tests can be ran without the docker compose setup.

Some tests require custom responses, for example to retrieve the ``subjectIdentificatie``
when a ``subject`` URL is supplied. For these cases a ``test_server.py`` file is added
that can be modified as needed to create a response for a cassette.
