.. _installation_prerequisites:

Prerequisites
=============

Open Klant is most often deployed as a Docker container. While the
`container images <https://hub.docker.com/r/maykinmedia/open-klant/>`_ contain all the
necessary dependencies, Open Klant does require extra service to deploy the full stack.
These dependencies and their supported versions are documented here.

The ``docker-compose.yml`` (not suitable for production usage!) in the root of the
repository also describes these dependencies.

PostgreSQL
----------

.. warning::

   Since Open Klant version 2.10.0, PostgreSQL version 14 or higher is required. Attempting
   to deploy this version of Open Klant with PostgreSQL 13 or lower will result in errors!

Open Klant currently only supports PostgreSQL as datastore.

The supported versions in the table below are tested in the CI pipeline.

================ =========== ======= ======= ======= =======
Postgres version 13 or lower 14      15      16      17
================ =========== ======= ======= ======= =======
Supported?       |cross|     |check| |check| |check| |check|
================ =========== ======= ======= ======= =======

.. warning:: Open Klant only supports maintained versions of PostgreSQL. Once a version is
   `EOL <https://www.postgresql.org/support/versioning/>`_, support will
   be dropped in the next release.

Redis
-----

Open Klant uses Redis as a cache backend, especially relevant for admin sessions, and as
task queue broker.

Supported versions: 5, 6, 7.

RabbitMQ
--------

Open Klant uses RabbitMQ as a message broker and has confirmed support for RabbitMQ
version 4.x. Other versions may work, but it is not guaranteed.

.. |check| unicode:: U+2705 .. ✅
.. |cross| unicode:: U+274C .. ❌
