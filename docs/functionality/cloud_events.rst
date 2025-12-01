.. _cloud_events_developer_docs:

Cloud events
------------

Open Klant can emit cloud events when configured to do so via the
``ENABLE_CLOUD_EVENTS`` setting.

Currently, Open Klant emits the following cloud event:

* ``zaak-gelinkt``: emitted when an ``Onderwerpobject`` is created that links to a
  Zaak (i.e. when ``codeObjecttype="zaak"`` in the ``onderwerpobjectidentificator`` field).

Cloud events are only sent when both of the following are true:

* ``ENABLE_CLOUD_EVENTS = True`` is set in Django settings, **and**
* ``NOTIFICATIONS_SOURCE`` is configured with a non-empty identifier.

If either of these settings is missing, cloud events will **not** be emitted.

Example of a ``zaak-gelinkt`` cloud event in its current shape:

.. code-block:: json

    {
        "specversion": "1.0",
        "type": "nl.overheid.zaken.zaak-gelinkt",
        "source": "ok-test",
        "subject": "a7b3c8d9-e4f5-6a7b-8c9d-e0f1a2b3c4d5",
        "id": "f347fd1f-dac1-4870-9dd0-f6c00edf4bf7",
        "time": "2025-10-10T00:00:00Z",
        "dataref": "/klantinteracties/api/v1/onderwerpobjecten/12345678-aaaa-bbbb-cccc-999999999999",
        "datacontenttype": "application/json",
        "data": {
            "zaak": "urn:uuid:a7b3c8d9-e4f5-6a7b-8c9d-e0f1a2b3c4d5",
            "linkTo": "/klantinteracties/api/v1/onderwerpobjecten/12345678-aaaa-bbbb-cccc-999999999999",
            "label": "Mijn Klantcontact Onderwerp",
            "linkObjectType": "Onderwerpobject"
        }
    }

The shape of these cloud events and the actions that trigger them are still subject to
change. Currently, cloud events are delivered directly to the configured endpoint of
Open Notificaties, but in the future it will be possible to route these cloud events
using Open Notificaties message routing as well.

