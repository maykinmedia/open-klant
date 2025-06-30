.. _manual_logging:

Logging
=======

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

Open Klant log events
----------------------

Below is the list of logging ``event`` types that Open Klant can emit. In addition to the mentioned
context variables, these events will also have the **request bound metadata** described in the :ref:`django-structlog documentation <request_events>`.

API
~~~

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

Setup configuration
~~~~~~~~~~~~~~~~~~~

* ``no_tokens_defined``: while running the token configuration step, it was detected that the config file did not define any tokens.
* ``configuring_token``: attempting to configure a token. Additional context: ``token_identifier``.
* ``no_validation_errors_found``: no validation error found for the token. Additional context: ``token_identifier``.
* ``save_token_to_database``: attempting to save a token to the database. Additional context: ``token_identifier``.
* ``token_configuration_failure``: configuring a token failed. Additional context: ``token_identifier``, ``exc_info``.
* ``token_configuration_success``: configuring a token succeeded. Additional context: ``token_identifier``.


Third party library events
--------------------------

For more information about log events emitted by third party libraries, refer to the documentation
for that particular library

* :ref:`Django (via django-structlog) <request_events>`
* :ref:`Celery (via django-structlog) <request_events>`
