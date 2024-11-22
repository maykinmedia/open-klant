==============
Change history
==============

2.4.0
=====
*November, 22, 2024*

**New features**

* [#287] Added admin inlines for the ``InterneTaak`` and ``Actor`` to allow managing
  the relations between both. Also added search fields for both admins to search for both relations.
* [#197] Added a ``migrate_to_v2`` management command which allows users of version ``1.0.0`` to migrate to version ``2.4.0``
  More information can be found in the `documentation <https://open-klant.readthedocs.io/en/latest/installation/migration.html>`
* [#246] Added ``is_standaard_adres`` for ``DigitaalAdres``
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
* [#261] Fixed ``Onderwerpobject`` inline to use ``klantcontact``
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
