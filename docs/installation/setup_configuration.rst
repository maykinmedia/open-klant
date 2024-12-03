.. _installation_configuration_cli:

==============================
Open Klant configuration (CLI)
==============================

After deploying Open Klant, it needs to be configured to be fully functional.
You can get the full command documentation with:

.. code-block:: bash

    ./src/manage.py setup_configuration --help

.. warning:: This command is declarative - if configuration is manually changed after
   running the command and you then run the exact same command again, the manual
   changes will be reverted.

Preparation
===========

The command executes the list of pluggable configuration steps, and each step
has required specific variables, that should be prepared.
Here is the description of all available configuration steps and the variables,
used by each step.

Token configuration
----------------------

Create a YAML configuration file with your settings:

.. code-block:: yaml

    tokens_config_enable: true

    tokens_config:
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

.. note:: Invalid entries will be skipped and logged according to the configured
   logging settings.

Execution
=========

Open Klant configuration
------------------------

With the full command invocation, everything is configured at once. Each configuration step
is idempotent, so any manual changes made via the admin interface will be updated if the command
is run afterwards.

.. code-block:: bash

    ./src/manage.py setup_configuration --yaml-file /path/to/config.yaml

.. note:: Due to a cache-bug in the underlying framework, you need to restart all
   replicas for part of this change to take effect everywhere.
