.. _referentielijsten_configuration:

Referentielijsten API Integration
=================================

Overview
--------

Open Klant allows municipalities to record customer interactions via `/klantcontact`.
Each `klantcontact` must include a `kanaal` (channel).

By default, the `kanaal` field is a simple string (max 50 characters) without strict validation.
This can lead to inconsistent data across applications (for example: ``'email'`` vs ``'e-mail'``).

Optional Integration
--------------------

Open Klant provides an optional integration with the Referentielijsten API. When enabled:

- The `kanaal` provided for a `/klantcontact` is validated against a configured table in the Referentielijsten API.
- Only kanalen currently valid (based on `begindatumGeldigheid` and `einddatumGeldigheid`) are allowed.
- If the `kanaal` is not found, a `ValidationError` is raised, listing all valid kanalen.

Municipality Responsibility
---------------------------

If kanalen are removed from the Referentielijsten table, it is the municipality's responsibility to ensure that existing `Klantcontact.kanaal` values in Open Klant remain correct.

Status Check
------------

For verification, Open Klant can perform a status check that:

- Returns the HTTP status code of the GET request to the Referentielijsten table.
- Optionally returns the list of kanalen.

This allows verification that the connection is working and the expected kanalen are returned.
