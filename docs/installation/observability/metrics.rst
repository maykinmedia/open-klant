.. _installation_observability_metrics:

=======
Metrics
=======

Open Klant produces application metrics (using Open Telemetry).

.. note:: The exact metric names that show up may be transformed, e.g. Prometheus replaces
   periods with underscores, and processing pipelines may add prefixes or suffixes.

.. important:: Some metrics are defined as "global scope".

   These metrics are typically derived from application state introspection, e.g. by
   performing database (read) queries to aggregate some information. Usually those
   correspond to an `Asynchronous Gauge <https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-gauge>`_.

   Multiple replicas and/or instances of the same service will produce the same values
   of the metrics. You need to apply some kind of aggregation to de-duplicate these
   values. The attribute ``scope="global"``  acts as a marker for these type of metrics.

   With PromQL for example, you can use ``avg`` on the assumption that all values will
   be equal, so the average will also be identical:

   .. code-block:: promql

       avg by (type) (otel_user_count{scope="global"})

Generic
=======

``http.server.duration``
    Captures how long each HTTP request took, in ms. The metric produces histogram data.

``http.server.request.duration`` (not active)
    The future replacement of ``http.server.duration``, in seconds. Currently not
    enabled, but the code is in the Open Telemetry SDK instrumentation already and could
    possibly be opted-in to.

Application specific
====================

Accounts
--------

``user_count``
    Reports the number of users in the database. This is a global metric, you must take
    care in de-duplicating results. Additional attributes are:

    - ``scope`` - fixed, set to ``global`` to enable de-duplication.
    - ``type`` - the user type. ``all``, ``staff`` or ``superuser``.

    Sample PromQL query:

    .. code-block:: promql

        max by (type) (last_over_time(
          otel_user_count{scope="global"}
          [1m]
        ))

``auth.login_failures``
    A counter incremented every time a user login fails (typically because of invalid
    credentials). Does not include the second factor, if enabled. Additional attributes:

    - ``http_target`` - the request path where the login failure occurred, if this
      happened in a request context.

``auth.user_lockouts``
    A counter incremented every time a user is locked out because they reached the
    maximum number of failed attempts. Additional attributes:

    - ``http_target`` - the request path where the login failure occurred, if this
      happened in a request context.
    - ``username`` - username of the user trying to log in.

``auth.logins``
    Counter incrementing on every successful login by a user. Additional attributes:

    - ``http_target`` - the request path where the login failure occurred, if this
      happened in a request context.
    - ``username`` - username of the user trying to log in.

``auth.logouts``
    Counter incrementing every time a user logs out. Additional attributes:

    - ``username`` - username of the user who logged out.

Klantcontacten
--------------


``klantcontacten.create``
    Reports the number of klantcontacten created via the API.

``klantcontacten.update``
    Reports the number of klantcontacten updated via the API.

``klantcontacten.delete``
    Reports the number of klantcontacten deleted via the API.

The klantcontacten metrics show how many entities are created, updated, or deleted via the API,
helping to monitor load and the most frequent operations, and allow for various aggregations on the data.

    Sample PromQL query:

    .. code-block:: promql

        sum by (otel_scope_name) (otel_klantcontacten_update_total)

Betrokkenen
-----------

``betrokkenen.create``
    Reports the number of betrokkenen created via the API.

``betrokkenen.update``
    Reports the number of betrokkenen updated via the API.

``betrokkenen.delete``
    Reports the number of betrokkenen deleted via the API.

The betrokkenen metrics show how many entities are created, updated, or deleted via the API,
helping to monitor load and the most frequent operations, and allow for various aggregations on the data.

    Sample PromQL query:

    .. code-block:: promql

        sum by (otel_scope_name) (otel_betrokkenen_update_total)

Partijen
--------

``partijen.create``
    Reports the number of partijen created via the API.

``partijen.update``
    Reports the number of partijen updated via the API.

``partijen.delete``
    Reports the number of partijen deleted via the API.

The partijen metrics show how many entities are created, updated, or deleted via the API,
helping to monitor load and the most frequent operations, and allow for various aggregations on the data.

    Sample PromQL query:

    .. code-block:: promql

        sum by (otel_scope_name) (otel_partijen_update_total)

Actoren
-------

``actoren.create``
    Reports the number of actoren created via the API.

``actoren.update``
    Reports the number of actoren updated via the API.

``actoren.delete``
    Reports the number of actoren deleted via the API.

The actoren metrics show how many entities are created, updated, or deleted via the API,
helping to monitor load and the most frequent operations, and allow for various aggregations on the data.

    Sample PromQL query:

    .. code-block:: promql

        sum by (otel_scope_name) (otel_actoren_update_total)

Digitale Adressen
-----------------

``digitale_adressen.create``
    Reports the number of digitale adressen created via the API.

``digitale_adressen.update``
    Reports the number of digitale adressen updated via the API.

``digitale_adressen.delete``
    Reports the number of digitale adressen deleted via the API.

The digitale adressen metrics show how many entities are created, updated, or deleted via the API,
helping to monitor load and the most frequent operations, and allow for various aggregations on the data.

    Sample PromQL query:

    .. code-block:: promql

        sum by (otel_scope_name) (otel_digitale_adressen_update_total)

Interne Taken
-------------

``interne_taken.create``
    Reports the number of interne taken created via the API.

``interne_taken.update``
    Reports the number of interne taken updated via the API.

``interne_taken.delete``
    Reports the number of interne taken deleted via the API.

The interne taken metrics show how many entities are created, updated, or deleted via the API,
helping to monitor load and the most frequent operations, and allow for various aggregations on the data.

    Sample PromQL query:

    .. code-block:: promql

        sum by (otel_scope_name) (otel_interne_taken_update_total)
