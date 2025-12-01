.. _referentielijsten_configuration:

Referentielijsten API Integration
=================================

Overview
--------

Open Klant allows municipalities to record customer interactions via the `/klantcontacten` endpoint.
Each `klantcontact` must include a `kanaal` (channel).

By default, the `kanaal` field is a simple string (max 50 characters) without strict validation.
This can lead to inconsistent data across applications (for example: ``'email'`` vs ``'e-mail'``).

Optional Integration
--------------------

Open Klant provides an optional integration with the Referentielijsten API (see `documentation`_).

When enabled:

- The `kanaal` provided for a `/klantcontact` is validated against a configured table in the Referentielijsten API.
- Only kanalen currently valid (based on `begindatumGeldigheid` and `einddatumGeldigheid`) are allowed.
- If the `kanaal` is not found, a ``400`` error is raised, listing all valid kanalen.

This integration can be configured in the admin interface via **Configuratie > Referentielijsten configuration**
or through the ``django-setup-configuration``. For detailed instructions, see the
:ref:`setup configuration  <ref_step_openklant.setup_configuration.steps.ReferentielijstenConfigurationStep>`.

Maintenance
-----------

If kanalen are removed from the Referentielijsten table, it is the municipality's
responsibility to ensure that existing `Klantcontact.kanaal` values in Open Klant remain correct,
because there could still be `klantcontacten` in the database that use this removed kanaal.
The same applies for kanalen that are no longer valid, because the `einddatumGeldigheid` has been reached.

.. _documentation: https://referentielijsten-api.readthedocs.io/en/latest/
