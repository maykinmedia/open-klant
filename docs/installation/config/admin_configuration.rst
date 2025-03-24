.. _installation_admin_config:


================================
Open Klant configuration (admin)
================================

Before you can work with Open Klant after installation, a few settings need to be
configured first.

.. note::

    This document describes the manual configuration via the admin. You can perform
    most of this configuration via the :ref:`command line <installation_configuration_cli>`.
    which is both faster and less error prone.

.. _installation_configuration_token_authorization:

Create an API Token
===================

Open Klant
----------
By creating an API token, we can perform an API test call to verify the successful
installation.

1. Configure the Token authorizations for the Open Klant:

   a. **Api Auth** > **Token authorizations**
   b. Select Click **Token authorization toevoegen** (or select the token if it already exists).
   c. Fill out the form:

      - **Identifier**: *For example:* ``token-1``
      - **Contact person**: *For example:* ``Person 1``
      - **Email**: *For example:* ``test@example.com``
      - **Organization**: *For example:* ``Organization XYZ``
      - **Application**: *For example:* ``Application XYZ``
      - **Administration**: *For example:* ``Administration XYZ``
   
   d. Click **Opslaan**.

After creating the **Token**, the **key** can be used in the ``Authorization`` header for make the requests. 
Example of an API call here :ref:`command line <installation_configuration_api_call>`,

.. _installation_configuration_notificaties_api:

Configure Notificaties API
==========================

Next, if notifications are enabled using the ``NOTIFICATIONS_ENABLED`` environment variable
(see :ref:`installation_env_config` for more information), the notifications for Open Klant must be configured. 
We assume you're also using Open Notificaties to make a complete setup.

Open Klant
----------

The configuration steps below need to be performed in Open Klant itself.

**Open Klant consuming the Notificaties API**

1. Configure the credentials for the Notificaties API (so Open Klant can access
   the Notificaties API):

   a. Navigate to **Overige > Services**
   b. Select Click **Service toevoegen** (or select the notifications service if
      it already exists).
   c. Fill out the form:

      - **Label**: *For example:* ``Open Notificaties``
      - **Service slug**: *For example:* ``open-notificaties``
      - **Type**: Select the option: ``NRC (Notifications)``
      - **API root url**: the full URL to the Notificaties API root, e.g.
        ``https://notificaties.gemeente.local/api/v1/``

      - **Client ID**: An existing Client ID for the notifications service, or create
        one and configure the same value in Open Notificaties - *For example:* ``open-klant``
      - **Secret**: *Some random string. You will need this later on!*
      - **Authorization type**: Select the option: ``ZGW client_id + secret``
      - **OAS url**: URL that points to the OpenAPI specification. This is typically
        ``<API-ROOT>/schema/openapi.yaml``, *for example:*
        ``https://notificaties.gemeente.local/api/v1/schema/openapi.yaml``
      - **User ID**: *Same as the Client ID*
      - **User representation**: *For example:* ``Open Klant``

   d. Click **Opslaan**.

2. Next, configure Open Klant to use this service for the Notificaties API:

   a. Navigate to **Overige > Notificatiescomponentconfiguratie**
   b. Select the service from the previous step in the **Notifications api service**
      dropdown.
   c. Sending notifications support autoretry mechanism, which can be also configured here.
      Fill out the following properties:

      - **Notification delivery max retries**: the maximum number of retries the task queue
        will do if sending a notification failed. Default is ``5``.
      - **Notification delivery retry backoff**: a boolean or a number. If this option is set to
        ``True``, autoretries will be delayed following the rules of exponential backoff. If
        this option is set to a number, it is used as a delay factor. Default is ``3``.
      - **Notification delivery retry backoff max**: an integer, specifying number of seconds.
        If ``Notification delivery retry backoff`` is enabled, this option will set a maximum
        delay in seconds between task autoretries. Default is ``48`` seconds.
   d. Click **Opslaan**.


Open Notificaties
-----------------

1. We need to allow Open Klant to access Open Notificaties (for
   authentication purposes, so we can then check its authorisations):

   a. Navigate to **API Autorisaties > Autorisatiegegeven**
   b. Click **Autorisatiegegeven toevoegen**.
   c. Fill out the form:

      - **Client ID**: *The same Client ID as given in Open Klant step 1c*.
        *For example:* ``open-klant``
      - **Secret**: *The same Secret as given in Open Klant step 1c*

   d. Click **Opslaan**.

2. We have to check also the Applicatie is setted in Open Notificaties:

   a. Navigate to **API Autorisaties > Applicaties**
   b. Click **Applicatie toevoegen**.
   c. Fill out the form:

      - **Client ID**: *The same Client ID as given in Open Klant step 1c*.
        *For example:* ``open-klant``
      - **Label**: *For example:* ``Open Klant``

   d. Click **Opslaan**.

All done!
Now Open Klant and Open Notificaties can access each other.


Register Notification channels
------------------------------

Before notifications can be sent to ``kanalen`` in Open Notificaties, these ``kanalen``
must first be registered via Open Klant.

.. warning::  
   Ensure that the ``SITE_DOMAIN`` environment variable is correctly set before registering channels,
   as it defines the source from which the channels are retrieved. 
   For more details, see :ref:`Environment configuration reference <installation_env_config>` for the full list of available variables 
   and how to configure them.
   

Register the required channels:

.. code-block:: bash

    python src/manage.py register_kanalen


.. _installation_configuration_api_call:

Making an API call
==================

Open Klant
----------

We can now make an HTTP request to one of the APIs of Open Klant. For this
example, we have used `curl`_ to make the request.

.. code-block:: bash

   curl --request GET \
   --header 'Authorization: Token ba9d233e95e04c4a8a661a27daffe7c9bd019067' \
   --header 'Content-Type: application/json' \
   {{base_url}}/klantinteracties/api/v1/partijen

.. _Curl: https://curl.se/docs/manpage.html
