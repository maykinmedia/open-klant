.. _installation_configuration_cli:

==============================
Open Klant configuration (CLI)
==============================

After deploying Open Klant, it needs to be configured to be fully functional.
The django management command ``setup_configuration`` assist with this configuration.
You can get the full command documentation with:

.. code-block:: bash

    python ./src/manage.py setup_configuration --help

.. warning:: This command is declarative - if configuration is manually changed after
   running the command and you then run the exact same command again, the manual
   changes will be reverted.

Preparation
===========

The command executes the list of pluggable configuration steps, and each step
requires specific configuration information, that should be prepared.
Here is the description of all available configuration steps and the configuration
format, used by each step.

Token configuration
----------------------

Create a (single) YAML configuration file with your settings:

.. code-block:: yaml

    openklant_tokens_config_enable: true
    openklant_tokens:
      group:
        - identifier: token-1
          contact_person: Person 1
          email: person-1@example.com
          organization: Organization XYZ # optional
          application: Application XYZ # optional
          administration: Administration XYZ # optional

        - identifier: token-2
          contact_person: Person 2
          email: person-2@example.com


Mozilla-django-oidc-db
----------------------

Create or update the (single) YAML configuration file with your settings:

.. code-block:: yaml

   ...
    oidc_db_config_enable: true
    oidc_db_config_admin_auth:
      oidc_rp_client_id: client-id
      oidc_rp_client_secret: secret
      endpoint_config:
        oidc_op_discovery_endpoint: https://keycloak.local/protocol/openid-connect/
   ...

More details about configuring mozilla-django-oidc-db through ``setup_configuration``
can be found at the _`documentation`: https://mozilla-django-oidc-db.readthedocs.io/en/latest/setup_configuration.html.

Execution
=========

Open Klant configuration
------------------------

With the full command invocation, everything is configured at once. Each configuration step
is idempotent, so any manual changes made via the admin interface will be updated if the command
is run afterwards.

.. code-block:: bash

    python ./src/manage.py setup_configuration --yaml-file /path/to/config.yaml

.. note:: Due to a cache-bug in the underlying framework, you need to restart all
   replicas for part of this change to take effect everywhere.
