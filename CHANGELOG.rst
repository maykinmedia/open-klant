==============
Change history
==============

2.12.1
======
*September 4, 2025*

**Bugfixes**

* [:open-klant:`492`] Ensure 8 digit BSNs get a leading 0 in ``migrate_to_v2`` script

2.12.0
======
*August 28, 2025*

**New features**

* [:open-klant:`419`] Added query parameters on `onderwerpobjecten` for searching klantcontacten by referred klantcontact:

    * ``klantcontact__uuid``
    * ``klantcontact__url``
    * ``was_klantcontact__uuid``
    * ``was_klantcontact__url``

**Bugfixes/QOL**

* [:open-klant:`470`] Change ``countrycode`` validation message to warn when the value has incorrect casing.

**Documentation**

* [:open-api-framework:`159`] Add functionality to create model image (see :ref:`uml_diagrams`)

**Maintenance**

* Upgrade python dependencies

  * ``zgw-consumers`` to 1.0.0
  * ``commonground-api-common`` to 2.9.0
  * ``mozilla-django-oidc-db`` to 0.25.1

* [:open-api-framework:`179`] Add monkeypatch to requests applying a default timeout to all requests calls

2.11.1
======
*August 8, 2025*

**Bugfixes/QOL**

Fixes for ``migrate_to_v2`` command:

* [:open-klant:`459`] Ensure created Partijen with BSN/KVK have related partij-identificatoren
* [:open-klant:`459`] Allow passing of ``CLIENT_ID`` and ``SECRET`` envvars to generate access token (see :ref:`migration_user_docs`)
* [:open-klant:`459`] Set ``referentie`` to ``"portaalvoorkeur"`` for all DigitaalAdressen

2.11.0
======
*August 5, 2025*

**New features**

* [:open-klant:`437`] Add ``verificatieDatum`` attribute to ``DigitaalAdres``, as well as new query parameters

  * ``verificatieDatum``: match objects that have a ``verificatieDatum`` that is exactly this value
  * ``verificatieDatum__gt``: match objects that have a ``verificatieDatum`` greater than this value
  * ``verificatieDatum__gte``: match objects that have a ``verificatieDatum`` greater than or equal to this value
  * ``verificatieDatum__lt``: match objects that have a ``verificatieDatum`` less than this value
  * ``verificatieDatum__lte``: match objects that have a ``verificatieDatum`` less than or equal to this value
  * ``isGeverifieerd``: match objects that have a ``verificatieDatum``

**Bugfixes**

* [:open-klant:`457`] Fix bug that caused deletes on ``DigitaalAdres`` to cascade to ``Partij`` (via ``voorkeurs_digitaal_adres``)
* [:open-klant:`400`] Fix error when using ``expand`` due to the value of the attribute being ``None`` for some of the results
* [:open-klant:`454`] Ensure ``DB_CONN_MAX_AGE`` can be set via envvar
* Fix issue that caused Elastic APM to not show time spent on queries when connection pooling is enabled

**Maintenance**

* Upgrade python dependencies

  * ``celery`` to 5.5.3 (to fix Redis reconnection issues)
  * ``billiard`` to 4.2.1
  * ``django-privates`` to 3.1.1
  * ``open-api-framework`` to 0.12.0
  * ``commonground-api-common`` to 2.7.0

* Remove unused ``coreapi`` dependency
* [:open-klant:`465`] Upgrade NPM packages to fix security issues
* Move database connection pooling envvars to ``open-api-framework``
* Add missing ``bump-my-version`` dependency to dev deps

**Documentation**

* [:open-klant:`191`] Add Contactgegevens API links to README
* [:open-api-framework:`148`] Add prerequisites docs page (including PostgreSQL compatibility)

2.10.0
======
*July 4, 2025*

.. warning::

    This release upgrades Django to version 5.2.3, which requires PostgreSQL version 14 or higher.
    Attempting to deploy with PostgreSQL <14 will cause errors during deployment.

**New features**

.. note::

  The logging format has been changed from unstructured to structured with `structlog <https://www.structlog.org/en/stable/>`_.
  For more information on the available log events and their context, see :ref:`manual_logging`.

* [:open-klant:`434`] Add structlog for observability
* [:open-klant:`445`] Add log events for ``create``, ``update``, and ``delete`` operations on all API endpoints
* [:open-api-framework:`149`] Add dark/light theme toggle to the admin interface
* [:open-klant:`426`] Add environment variables for database connection pooling (see :ref:`installation_env_config` for more information)

  * DB_POOL_ENABLED
  * DB_POOL_MIN_SIZE
  * DB_POOL_MAX_SIZE
  * DB_POOL_TIMEOUT
  * DB_POOL_MAX_WAITING
  * DB_POOL_MAX_LIFETIME
  * DB_POOL_MAX_IDLE
  * DB_POOL_RECONNECT_TIMEOUT
  * DB_POOL_NUM_WORKERS
  * DB_CONN_MAX_AGE

**Bugfixes**

* [:open-klant:`418`] Fix incorrect URL reverse in ``csrf_failure`` function
* [:open-klant:`424`] Fix error in ``digitaleadressen`` endpoint when handling different digital address types

**Project maintenance**

* [:open-api-framework:`151`] Move ``ruff`` and ``bump-my-version`` configurations into ``pyproject.toml``

* Upgrade dependencies:

  * django to 5.2.3
  * notifications-api-common to 0.7.3
  * open-api-framework to 0.11.0
  * commonground-api-common to 2.6.7
  * django-setup-configuration to 0.8.2
  * django-debug-toolbar to 5.2.0
  * django-webtest to 1.9.13
  * zgw-consumers to 0.38.0
  * pyjwt to 2.10.1
  * requests to 2.32.4
  * urllib3 to 2.5.0
  * vcrpy to 7.0.0
  * platformdirs to 4.3.8

**Documentation**

* [:open-klant:`434`] Add documentation for logging


2.9.0
=====
*May 28, 2025*

**New features**

* [:open-klant:`338`] Add ``isStandaardAdres`` to the list endpoint filters for DigitaalAdres
* [:open-klant:`388`] Explicitly state in OAS that a space is required for postcodes
* [:open-klant:`417`] Add missing help texts in OAS for query parameters for ``onderwerpobjecten``, ``partij-identificatoren``, ``rekeningnummers`` and ``bijlagen``

**Bugfixes**

* Do not use ``save_outgoing_requests`` log handler if ``LOG_REQUESTS`` is set to false
* [:open-klant:`351`] Remove overig from partijidentificator and deprecate ``anderePartijIdentificator``

.. warning::

    The field ``anderePartijIdentificator`` for ``/partij-identificatoren`` endpoint is now deprecated and will be removed in the next major release

**Project maintenance**

* Upgrade dependencies

  * tornado to 6.5.1
  * open-api-framework to 0.10.1
  * commonground-api-common to 2.6.4

* Replace OAS GitHub actions workflows with single workflow
* [:open-api-framework:`132`] Remove ``pytest`` and ``check_sphinx.py``, replace with simpler commands
* [:open-api-framework:`133`]  Replace ``black``, ``isort`` and ``flake8`` with ``ruff`` and update code-quality workflow


2.8.0
=====
*May 14, 2025*


**New features**

* [:open-klant:`320`] Add ``DigitaalAdres.referentie`` and allow filtering on this attribute with the ``referentie`` query parameter
* [:open-klant:`368`] Fix validation for phone numbers
* [:open-klant:`240`] Make nullable fields optional for all endpoints
* [:open-klant:`342`] Add PartijIdentificator filters to ``/klantcontacten``, ``/betrokkenen`` and ``/digitaleadressen``
* [:open-klant:`391`] Make ``huisnummer`` nullable via the API
* [:open-klant:`395`] Integrate ``django-upgrade-check`` to ensure that all required OpenKlant versions are correctly handled during instance upgrades

**Bugfixes**

* [:open-klant:`378`] Fix bug that occurred when trying to create a ``Partij`` via the admin interface and improve admin performance
* [:open-klant:`341`] Add missing help texts for several query parameters in the API schema
* [:open-klant:`401`] Fix PATCH requests on ``/partijen/{uuid}`` if ``digitaleAdressen`` and/or ``rekeningnummers`` are set to ``null``
* [:open-klant:`345`] No longer make ``Partij.soortPartij`` required for PATCH requests

**Project maintenance**

* Upgrade commonground-api-common to 2.6.3
* Upgrade NPM http-proxy-middleware to 2.0.9
* [:open-klant:`395`] Upgrade to Python 3.12
* [:open-klant:`385`] Improve performance of several endpoints

.. note::

  Used ``select_related`` and ``prefetch_related`` to minimize query count and improve efficiency, improving key endpoints such as ``/actoren``, ``/partijen``, ``/partij-identificatoren``, ``/klantcontacten``

**Documentation**

* [:open-klant:`249`] Add default to the help text of the ``pageSize`` attribute
* [:open-klant:`363`] Update documentation for ``Partij`` and ``PartijIdentificator``
* [:open-klant:`337`] Change help texts for ``onderwerpobjectidentificator``
* [:open-klant:`408`] Fix notifications documentation by replacing ``NOTIFICATIONS_ENABLED`` with ``NOTIFICATION_DISABLED``


2.7.0
=====
*April, 3, 2025*


**New features**

* [:open-klant:`212`] Add ``digitaleAdressen`` as expand option for ``/betrokkenen`` endpoint
* [:open-klant:`239`] Accept Partij Identificatoren as part of Partij creation
* [:open-klant:`355`] Add Notifications for InterneTaak and Partij (see :ref:`installation_configuration_notificaties_api`)

.. note::

  Additional configuration steps have been introduced to set up external services and notifications through ``django-setup-configuration`` (see :ref:`installation_configuration_cli`)

* [:open-api-framework:`59`] Remove ``django.contrib.sites`` dependency

.. warning::

    To save the domain of the application you have to declare the environment variable ``SITE_DOMAIN`` (see :ref:`installation_env_config` > Optional for more information)

**Bugfixes**

* [:open-klant:`376`] Fix camelCase naming for query parameters in GET requests

**Project maintenance**

* [:open-api-framework:`115`] Fix OAS check github action
* [:open-api-framework:`116`] Fix codecov publish
* [:open-api-framework:`117`] Upgrade version of CI dependencies

  * Confirm support for Postgres 17
  * Development tools: black to 25.1.0, flake8 to 7.1.2 and isort to 6.0.1
  * Upgrade GHA versions
  * Upgrade nodejs to 20

* Remove ``changed-files`` actions from CI and moved in a separate script
* Remove duplicate CodeQL workflow
* Fix ``bump-my-version`` for package/package-lock.json
* Upgrade dependencies

  * Upgrade coverage to 7.7.0
  * Upgrade cryptography to 44.0.2
  * Upgrade jinja2 to 3.1.6
  * Upgrade kombu to 5.5.2
  * Upgrade django to 4.2.20
  * Upgrade django-setup-configuration to 0.7.2
  * Upgrade open-api-framework to 0.9.6
  * Upgrade notifications-api-common to 0.7.2
  * Upgrade commonground-api-common to 2.5.5

**Documentation**

* Update documentation for configurations


2.6.1
=====
*March, 21, 2025*

**Bugfixes**

* [:open-klant:`369`] Ensure PartijIdentificator.partij can be null


2.6.0
=====
*March, 4, 2025*

**New features**

* [:open-klant:`233`] Fix set of values for PartijIdentificatoren (ENUM)
* [:open-klant:`267`] Enforce uniqueness of Partij and PartijIdentificatoren
* [:open-klant:`309`] Add separate fields for Dutch addresses next to address lines 1 to 3
* [:open-klant:`310`] Update BAG ID fields with new validations
* [:open-klant:`311`] Update country codes fields with ISO 3166

.. warning::

    Issues ``#311``, ``#310``, ``#267`` modify existing fields and add new constraints to models, which can cause them to break,
    as some previous values will no longer be valid.
    During migration, invalid values are logged so that they can be fixed manually and then migrations have to be executed again.


**Project maintenance**

* Upgrading dependencies:

  * Upgrade open-api-framework to 0.9.3
  * Upgrade Django to 4.2.19
  * Upgrade cryptography to 44.0.1
  * [:open-klant:`324`] Upgrade django-setup-configuration to 0.7.1
  * [:open-klant:`324`] Upgrade mozilla-django-oidc-db to 0.22.0
* [:open-api-framework:`79`] Disable admin nav sidebar
* [:open-api-framework:`99`] Add quick-start workflow to test docker-compose.yml
* [:open-api-framework:`107`] Add release template
* [:open-klant:`299`] Add Nginx to Open Klant helm chart

**Documentation**

* Improvements to documentation structure and configuration steps (CLI and Admin)


2.5.0
=====
*January, 28, 2025*

**New features**

* Add support for setup configuration
    * [#293] Configuring access tokens
    * [#294] Admin authentication via OIDC

**Bugfixes/QoL**:

* Add UUID to Klantinteracties admin search fields and fieldsets
* [#254] Fix incorrect URLs being returned in API responses for ``Persoon``, ``Bijlage`` and ``CategorieRelatie``
* [#265] Fix ``adres__icontains`` for GET requests on ``digitaleadressen`` endpoint
* [#272] Make ``digitaalAdres.omschrijving`` not required
* [#252] Make ``Persoon.overlijdensdatum`` optional via admin interface
* Point help text for ``DigitaalAdres.is_standaard_adres`` to correctly cased field name
* [maykinmedia/charts#148] Add timeouts to celery tasks


**Project maintenance**

* [#66] Update zgw-consumers to 0.35.1
* [#66] Update commonground-api-common to 2.1.2
* [#66] Update notifications-api-common to 0.3.1
* Update open-api-framework to 0.9.2
* [maykinmedia/open-api-framework#92] Make sure documentation is built in CI
* [maykinmedia/open-api-framework#92] Fix pushing of Docker latest tag
* Fix code-analysis workflow
* [maykinmedia/open-api-framework#81] Switch from pip-compile to UV
* [maykinmedia/open-api-framework#93] Security updates for third party libraries

**Documentation**

* Add documentation for OpenKlant v2 semantic information model


2.4.0
=====
*November, 26, 2024*

**New features**

* [#256] Added the ``hadBetrokkene__wasPartij__url`` and ``hadBetrokkene__wasPartij__uuid``
  query parameters to allow filtering ``KlantenContact`` by ``Partij``
* [#251] Added admin inlines for the ``InterneTaak`` and ``Actor`` to allow managing
  the relations between both. Also added search fields for both admins to search for both relations.
* [#197] Added a ``migrate_to_v2`` management command which allows users of version ``1.0.0`` to migrate to version ``2.4.0``
  More information can be found in the `documentation <https://open-klant.readthedocs.io/en/latest/installation/migration.html>`
* [#246] Added ``isStandaardAdres`` for ``DigitaalAdres``
* Updated OAF version to 0.9.0. This upgrade allows admin users managing their sessions through the admin.
* [#147] Added ``/maak-klantcontact`` convenience endpoint. This allows creating
  a ``KlantContact``, a ``Betrokkene`` and a ``OnderwerpObject`` through a
  single API request
* [#232] Added ``soortDigitaalAdres`` enum for ``DigitaalAdres``

**Bugfixes/QoL**:

* [#235] Added extra validation for phone numbers for ``DigitaalAdres.adres``
  when ``DigitaalAdres.soortDigitaalAdres`` is ``telefoonnummer``.
* [#243] Fix expand query parameters. Shows the ``_expand`` field in the response body
  even though it might be empty. This behavior is applied to all available
  ``_expand`` parameters.
* [#258] Added correct API root paths in redoc OAS
* [#234] Added validation for ``DigitaalAdres.adres`` when it's type is ``email``
* [#227] Fixed ``partijen`` creation endpoint crash when ``partijIdentificatie`` is not provided
* [#261] Fixed ``Onderwerpobject`` admin inline to use ``klantcontact`` instead of
  ``was_klantcontact``
* [#226] Made ``betrokkene`` a non-required form field in the admin
* [#229] Fixed partijen admin search

**Project maintenance**

* [#247] Added CI check to verify open API framework is updated to the latest version
* Upgraded commonground-api-common to 1.13.4
* [#13] Implemented open-api-workflows

2.3.0
=====
*October 4, 2024*

**New features**

* [#236] add dynamic pagination with ``pageSize`` parameter

**Bugfixes/QoL**:

* [#258] Use correct API root in redoc OAS
* [#255] Fix API schema not showing caused by CSP errors
* [#255] Change SameSite session cookie  to lax to fix OIDC login not working

2.2.0
=====

*September 5, 2024*

**New features**

* [#50] updated Python dependencies to minimize security risks.
* [#208] fixed the bug within the API schema generation for expand paths.
* [#209] added query parameters to the `digitaleadressen` endpoint.
* [#214] Added expand path from `digitaleadressen` to `internetaken`.
* [#182] added `actoren` field in `internetaken`.
* [#207] changed indicatie geheimhouding from required to optional.
* updated open-api-framework to 0.8.0, which includes adding CSRF, CSP and HSTS settings (#438).
  All new environment variables are added to the `documentation <https://objects-and-objecttypes-api.readthedocs.io/en/latest/installation/config.html>`_

.. warning::

    ``SECURE_HSTS_SECONDS`` has been added with a default of 31536000 seconds, ensure that
    before upgrading to this version of open-api-framework, your entire application is served
    over HTTPS, otherwise this setting can break parts of your application (see https://docs.djangoproject.com/en/4.2/ref/middleware/#http-strict-transport-security)

.. warning::

    With the introduction of the ``actoren`` field in the `internetaken` endpoint, the field ``actor`` is now deprecated and will be removed in the next version.

2.1.0
=====

*July 16, 2024*

**New features**:

* Add support for mounting Open Klant on a ``SUBPATH``
* Elastic APM service name can now be configured with ``ELASTIC_APM_SERVICE_NAME`` envvar
* [#175] added expand for detail endpoints in redoc
* Made user emails unique to prevent two users logging in with the same email, causing an error
* [#183] added afgehandeld_op field for internetaken
* [#189] Introduced two-factor authentification (2FA) for the Admin, which can be disabled by the environment variable ``DISABLE_2FA``

.. warning::

    The service name for Elastic APM is now configurable via the ``ELASTIC_APM_SERVICE_NAME`` environment variable.
    The default value changed from ``Open Klant - <ENVIRONMENT>`` to ``openklant - <ENVIRONMENT>``

.. warning::
    User email addresses will now be unique on a database level. The database migration will fail if there are already
    two or more users with the same email address. You must ensure this is not the case before upgrading.

.. warning::

    Two-factor authentication is enabled by default. The ``DISABLE_2FA`` environment variable
    can be used to disable it if needed.

**Bugfixes/QoL**:

* Settings module was refactored to use generic settings provided by Open API Framework
* [#187] Streamline environment variables
* Fix help-text icon for datetime field in the admin

**Documentation**

* [#196] remove links to outdated VNG documentation

**Project maintenance**

* [#179] Fix Trivy github action
* Update to Python 3.11
* [#155] use open-api-framework
* [#188] remove unused notification settings
* Refactor settings module


2.0.0
=====

*March 15, 2024*

*VNG officially retired the Klanten and Contactmomenten API, which never had an
official release. These API's are replaced by the Klantinteractie API. In
cooperation with several municipalities and VNG, Open Klant will implement the
new API specification and might introduce backwards incompatible changes. Since
Open Klant never had an official 1.0 release, we will continue versioning on
the 0.x.x-scheme.*

* Initial release of Open Klant featuring the first iteration of the
  Klantinteracties API.

1.0.0
=====

*February 16, 2023*

* Only a version change has been applied to emphasize the major change from
  version 1.0.0 to 2.0.0 which features a completely different API.

0.5.0-pre
=========

*August 5, 2023*

* [#51] Showing version & git hash on the home page

0.3.0-pre
=========

*July 24, 2023*

* [#50] Added Notificatie API support

0.2.0-pre
=========

*June 14, 2023*

* [#46] Fixed CI code-quality issues
* [#45] Updated docs and URLs to use new Github location
* [#44] Updated project dependencies
* [#48] Add missing auth to URLValidator for klantcontactmoment

0.1.0
=========

*February 13, 2023*

* Initial release.
