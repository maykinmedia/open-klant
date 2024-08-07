==============
Change history
==============

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
