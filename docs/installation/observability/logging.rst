.. _installation_observability_logging:

=======
Logging
=======

Logging is the practice of emitting log messages that describe what is happening in the
system, or "events" in short. Log events can have varying degrees of severity, such as
``debug``, ``info``, ``warning``, ``error`` or even ``critical``. By default, Open Klant
emits logs with level ``info`` and higher.

A collection of log events with a correlation ID (like a request or trace ID) allow one
to reconstruct the chain of events that took place which lead to a particular outcome.

Open Klant emits structured logs in JSON format (unless explicitly configured otherwise),
which should make log aggregation and analysis easier.

We try to keep a consistent log message structure, where the following keys
are (usually) present:

``source``
    The component in the application stack that produced the log entry. Typical
    values are ``uwsgi`` and ``app``.

``level``
    The severity level of the log message. One of ``debug``, ``info``, ``warning``,
    ``error`` or ``critical``.

``timestamp``
    The moment when the log entry was produced, a string in ISO-8601 format. Most of
    the logs have microsecond precision, but some of them are limited to second
    precision.

``event``
    The event that occurred, e.g. ``request_started`` or ``spawned worker (PID 123)``.
    This gives the semantic meaning to the log entry.

Other keys that frequently occur are:

``request_id``
    Present for application logs emitted during an HTTP request, makes it possible to
    correlate multiple log entries for a single request. Not available in logs emitted
    by background tasks or logs emitted before/after the Open Klant app.

.. tip:: Certain log aggregation solutions require you to configure "labels" to extract
   for efficient querying. You can use the above summary of log context keys to configure
   this according to your needs.

.. note:: We can not 100% guarantee that every log message will always be JSON due to
   limitations in third party software/packages that we use. Most (if not all) log
   aggregation technologies support handling both structured and unstructured logs.


.. _manual_logging:

Format
------

Open Klant emits structured logs (using `structlog <https://www.structlog.org/en/stable/>`_).
A log line can be formatted like this:

.. code-block:: json

    {
        "uuid": "1734afac-4628-446d-b344-f39b42f48bd9",
        "nummer": 1,
        "onderwerp": "test",
        "plaatsgevonden_op": "2025-06-16T14:09:20.339166Z",
        "token_identifier": "application-test",
        "token_application": "Application (test)",
        "event": "klantcontact_created",
        "user_id": null,
        "request_id": "2f9e9a5b-d549-4faa-a411-594aa8a52eee",
        "timestamp": "2025-05-19T14:09:20.339166Z",
        "logger": "openklant.components.klantinteracties.api.viewsets.klantcontacten",
        "level": "info"
    }

Each log line will contain an ``event`` type, a ``timestamp`` and a ``level``.
Dependent on your configured ``LOG_LEVEL`` (see :ref:`installation_env_config` for more information),
only log lines with of that level or higher will be emitted.

.. _manual_logging_exceptions:

Exceptions
~~~~~~~~~~

Handled exceptions follow a standardized JSON format to ensure consistency and improve error tracking.
Most fields are standard and include: ``title``, ``code``, ``status``, ``event``, ``source``, ``user_id``, ``request_id``, ``exception_id``, ``timestamp``, ``logger`` and ``level``.

A new field ``invalid_params`` has been added to provide detailed information about which input parameters caused the error in API calls:

    - ``name``: name of the invalid parameter
    - ``code``: specific error code
    - ``reason``: explanation/message of the error

.. code-block:: json

    {
        "title": "'Invalid input.'",
        "code": "invalid",
        "status": 400,
        "invalid_params": [
            {
                "name": "",
                "code": "",
                "reason": ""
            },
        ],
        "event": "api.handled_exception",
        "source": "app",
        "user_id": null,
        "request_id": "2f9e9a5b-d549-4faa-a411-594aa8a52eee",
        "exception_id": "55257460-13cc-40ca-890b-69c568dc1c5a",
        "timestamp": "2025-09-08T12:13:47.198478Z",
        "logger": "vng_api_common.exception_handling",
        "level": "error",
    }


Uncaught exceptions that occur via the API are logged as ``api.uncaught_exception`` events
and contain the traceback of the exception.

.. code-block:: json

    {
        "message": "division by zero",
        "event": "api.uncaught_exception",
        "request_id": "ad370b33-e200-42ca-ad3d-4911327b1255",
        "user_id": null,
        "timestamp": "2025-10-03T10:01:52.752639Z",
        "logger": "vng_api_common.views",
        "level": "error",
        "exception": "Traceback (most recent call last):\n  File \"/usr/local/lib/python3.12/site-packages/rest_framework/views.py\", line 506, in dispatch\n    response = handler(request, *args, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/usr/local/lib/python3.12/site-packages/drf_spectacular/drainage.py\", line 207, in wrapped_method\n    return method(self, request, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/usr/local/lib/python3.12/site-packages/rest_framework/mixins.py\", line 19, in create\n    self.perform_create(serializer)\n  File \"/usr/local/lib/python3.12/contextlib.py\", line 81, in inner\n    return func(*args, **kwds)\n           ^^^^^^^^^^^^^^^^^^^\n  File \"/app/src/openklant/components/klantinteracties/api/viewsets/digitaal_adres.py\", line 77, in perform_create\n    1 / 0\n    ~~^~~\nZeroDivisionError: division by zero"
    }


Open Klant log events
---------------------

Below is the list of logging ``event`` types that Open Klant can emit. In addition to the mentioned
context variables, these events will also have the **request bound metadata** described in the :ref:`django-structlog documentation <request_events>`.

API
~~~

* ``deprecated_endpoint_called``: a deprecated endpoint was called. Additional context: ``endpoint``.

* ``klantcontact_created``: created an ``Klantcontact`` via the API. Additional context: ``uuid``, ``nummer``, ``onderwerp``, ``plaatsgevonden_op``, ``token_identifier``, ``token_application``.
* ``klantcontact_updated``: updated an ``Klantcontact`` via the API. Additional context: ``uuid``, ``nummer``, ``onderwerp``, ``plaatsgevonden_op``, ``token_identifier``, ``token_application``.
* ``klantcontact_deleted``: deleted an ``Klantcontact`` via the API. Additional context: ``uuid``, ``nummer``, ``onderwerp``, ``plaatsgevonden_op``, ``token_identifier``, ``token_application``.
* ``klantcontact_geregistreerd``: created a ``Klantcontact``, ``Betrokkene`` and ``OnderwerpObject`` in a single call using the convenience endpoint.
  Additional context: ``uuid``, ``onderwerp``, ``plaatsgevonden_op``, ``token_identifier``, ``token_application``, ``betrokkene_uuid``, ``onderwerpobject_uuid``.
* ``organisatie_created`` / ``organisatie_updated`` / ``organisatie_deleted``:
  CRUD events for ``Organisatie``.
  Additional context: ``uuid``, ``token_identifier``, ``token_application``.
* ``persoon_created`` / ``persoon_updated`` / ``persoon_deleted``:
  CRUD events for ``Persoon``.
  Additional context: ``uuid``, ``token_identifier``, ``token_application``.
* ``actor_created`` / ``actor_updated`` / ``actor_deleted``:
  CRUD events for ``Actor``.
  Additional context: ``uuid``, ``token_identifier``, ``token_application``.
* ``digitaal_adres_created`` / ``digitaal_adres_updated`` / ``digitaal_adres_deleted``:
  CRUD events for ``DigitaalAdres``.
  Additional context: ``uuid``, ``partij_uuid``, ``betrokkene_uuid``, ``token_identifier``, ``token_application``.
* ``interne_taak_created`` / ``interne_taak_updated`` / ``interne_taak_deleted``:
  CRUD events for ``InterneTaak``.
  Additional context: ``uuid``, ``klantcontact_uuid``, ``token_identifier``, ``token_application``.
* ``betrokkene_created`` / ``betrokkene_updated`` / ``betrokkene_deleted``:
  CRUD events for ``Betrokkene``.
  Additional context: ``uuid``, ``partij_uuid``, ``klantcontact_uuid``, ``token_identifier``, ``token_application``.
* ``onderwerpobject_created`` / ``onderwerpobject_updated`` / ``onderwerpobject_deleted``:
  CRUD events for ``Onderwerpobject``.
  Additional context: ``uuid``, ``klantcontact_uuid``, ``was_klantcontact_uuid``, ``token_identifier``, ``token_application``.
* ``bijlage_created`` / ``bijlage_updated`` / ``bijlage_deleted``:
  CRUD events for ``Bijlage``.
  Additional context: ``uuid``, ``klantcontact_uuid``, ``token_identifier``, ``token_application``.
* ``actor_klantcontact_created`` / ``actor_klantcontact_updated`` / ``actor_klantcontact_deleted``:
  CRUD events for the relation between ``Actor`` and ``Klantcontact``.
  Additional context: ``uuid``, ``actor_uuid``, ``klantcontact_uuid``, ``token_identifier``, ``token_application``.
* ``partij_created`` / ``partij_updated`` / ``partij_deleted``:
  CRUD events for ``Partij``.
  Additional context: ``uuid``, ``organisatie_uuid``, ``persoon_uuid``, ``token_identifier``, ``token_application``.
* ``vertegenwoordiging_created`` / ``vertegenwoordiging_updated`` / ``vertegenwoordiging_deleted``:
  CRUD events for ``Vertegenwoordiging``.
  Additional context: ``uuid``, ``vertegenwoordigde_partij_uuid``, ``vertegenwoordigende_partij_uuid``, ``token_identifier``, ``token_application``.
* ``categorie_relatie_created`` / ``categorie_relatie_updated`` / ``categorie_relatie_deleted``:
  CRUD events for ``CategorieRelatie``.
  Additional context: ``uuid``, ``partij_uuid``, ``categorie_uuid``, ``token_identifier``, ``token_application``.
* ``categorie_created`` / ``categorie_updated`` / ``categorie_deleted``:
  CRUD events for ``Categorie``.
  Additional context: ``uuid``, ``token_identifier``, ``token_application``.
* ``partijidentificator_created`` / ``partijidentificator_updated`` / ``partijidentificator_deleted``:
  CRUD events for ``PartijIdentificator``.
  Additional context: ``uuid``, ``token_identifier``, ``token_application``.
* ``rekeningnummer_created`` / ``rekeningnummer_updated`` / ``rekeningnummer_deleted``:
  CRUD events for ``Rekeningnummer``.
  Additional context: ``uuid``, ``partij_uuid``, ``token_identifier``, ``token_application``.

Kanaal validation based on Referentielijsten integration
========================================================

There is an optional integration to validate ``Klantcontact.kanaal`` based on data in
the Referentielijsten API. The following log events can occur if this integration is enabled.

* ``missing_referentielijsten_service``: cannot perform ``kanaal`` validation to due missing service in configuration.
* ``failed_to_fetch_kanalen_from_referentielijsten``: something went wrong while trying to fetch the kanalen from
  Referentielijsten. Additional context: ``exc_info``.

Setup configuration
~~~~~~~~~~~~~~~~~~~

* ``no_tokens_defined``: while running the token configuration step, it was detected that the config file did not define any tokens.
* ``configuring_token``: attempting to configure a token. Additional context: ``token_identifier``.
* ``no_validation_errors_found``: no validation error found for the token. Additional context: ``token_identifier``.
* ``save_token_to_database``: attempting to save a token to the database. Additional context: ``token_identifier``.
* ``token_configuration_failure``: configuring a token failed. Additional context: ``token_identifier``, ``exc_info``.
* ``token_configuration_success``: configuring a token succeeded. Additional context: ``token_identifier``.
* ``configuring_referentielijsten``: attempting to configure Referentielijsten integration. Additional context: ``enabled``, ``service_identifier``.
* ``referentielijsten_configuration_failure``: configuration Referentielijsten integration failed.
* ``referentielijsten_configuration_success``: configuration Referentielijsten integration succeeded.

Third party library events
--------------------------

For more information about log events emitted by third party libraries, refer to the documentation
for that particular library

* :ref:`Django (via django-structlog) <request_events>`
* :ref:`Celery (via django-structlog) <request_events>`
