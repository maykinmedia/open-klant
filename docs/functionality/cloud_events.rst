.. _cloud_events_developer_docs:

Cloud events
------------

Open Klant can emit cloud events when configured to do so via the
``ENABLE_CLOUD_EVENTS`` setting.

Currently, Open Klant emits the following cloud event:

* ``nl.overheid.zaken.zaak-gekoppeld``: emitted when an ``Onderwerpobject`` is created or updated that links to a
  Zaak (i.e. when ``codeObjecttype="zaak"`` in the ``onderwerpobjectidentificator`` field).

Cloud events are only sent when both of the following are true:

* ``ENABLE_CLOUD_EVENTS = True`` is set in Django settings, **and**
* ``NOTIFICATIONS_SOURCE`` is configured with a non-empty identifier.

If either of these settings is missing, cloud events will **not** be emitted.

Example of a ``nl.overheid.zaken.zaak-gekoppeld`` cloud event in its current shape:

.. code-block:: json

    {
        "specversion": "1.0",
        "type": "nl.overheid.zaken.zaak-gekoppeld",
        "source": "urn:nld:oin:01823288444:openklant",
        "subject": "a7b3c8d9-e4f5-6a7b-8c9d-e0f1a2b3c4d5",
        "id": "f347fd1f-dac1-4870-9dd0-f6c00edf4bf7",
        "time": "2025-10-10T00:00:00Z",
        "datacontenttype": "application/json",
        "data": {
            "zaak": "urn:uuid:a7b3c8d9-e4f5-6a7b-8c9d-e0f1a2b3c4d5",
            "linkTo": "http://open-klant.local:8000/klantinteracties/api/v1/onderwerpobjecten/5fee9673-216c-41e7-91d2-69a8d1526b9f",
            "label": "Mijn Klantcontact Onderwerp",
            "linkObjectType": "Onderwerpobject"
        }
    }

*Note:* The ``subject`` field contains the UUID of the Zaak.

The shape of these cloud events and the actions that trigger them are still subject to
change.

In addition to linking events, Open Klant can also emit *unlink* events when a Zaak
is no longer related to an Onderwerpobject.

* ``nl.overheid.zaken.zaak-ontkoppeld``: emitted when a Zaak that was previously
  linked becomes unlinked. This happens when an ``Onderwerpobject`` that pointed
  to a Zaak is deleted, or otherwise changed such that the relationship with the
  Zaak disappears.

The payload of a ``nl.overheid.zaken.zaak-ontkoppeld`` event matches the shape of
the original ``zaak-gekoppeld`` event so that Open Zaak can correctly identify
and remove the corresponding ZaakObject relation.

Example of a ``nl.overheid.zaken.zaak-ontkoppeld`` cloud event:

.. code-block:: json

    {
        "specversion": "1.0",
        "type": "nl.overheid.zaken.zaak-ontkoppeld",
        "source": "urn:nld:oin:01823288444:openklant",
        "subject": "a7b3c8d9-e4f5-6a7b-8c9d-e0f1a2b3c4d5",
        "id": "f347fd1f-dac1-4870-9dd0-f6c00edf4bf7",
        "time": "2025-10-10T00:00:00Z",
        "datacontenttype": "application/json",
        "data": {
            "zaak": "urn:uuid:a7b3c8d9-e4f5-6a7b-8c9d-e0f1a2b3c4d5",
            "linkTo": "http://open-klant.local:8000/klantinteracties/api/v1/onderwerpobjecten/5fee9673-216c-41e7-91d2-69a8d1526b9f",
            "label": "Mijn Klantcontact Onderwerp",
            "linkObjectType": "Onderwerpobject"
        }
    }

*Note:* The ``subject`` field again contains the UUID of the Zaak.
