.. _cloud_events_developer_docs:

Cloud events
------------

Open Klant can emit cloud events when configured to do so via the
``ENABLE_CLOUD_EVENTS`` setting.

Currently, Open Klant emits the following cloud event:

* ``nl.overheid.zaken.zaak-gelinkt``: emitted when an ``Onderwerpobject`` is created that links to a
  Zaak (i.e. when ``codeObjecttype="zaak"`` in the ``onderwerpobjectidentificator`` field).

Cloud events are only sent when both of the following are true:

* ``ENABLE_CLOUD_EVENTS = True`` is set in Django settings, **and**
* ``NOTIFICATIONS_SOURCE`` is configured with a non-empty identifier.

If either of these settings is missing, cloud events will **not** be emitted.

Example of a ``nl.overheid.zaken.zaak-gelinkt`` cloud event in its current shape:

.. code-block:: json

    {
        "specversion": "1.0",
        "type": "nl.overheid.zaken.zaak-gelinkt",
        "source": "urn:nld:oin:01823288444:openzaak",
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
