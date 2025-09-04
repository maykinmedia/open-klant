.. _installation_observability:

=============
Observability
=============

Observability is an umbrella term for a number of principles and technologies to get
insight in running (distributed) systems. It typically focuses on Metrics, Logging and
Tracing, which provide insight in:

* what the application is doing, in particular as part of a larger system, such as
  microservice environments
* performance of the system
* how the system is used

Open Klant operates in distributed environments, and being able to fully trace a
customer request from start to end, observability tools are crucial. Below we provide
some additional context for infastructure teams that wish to integrate Open Klant in
their observability stack.

Logging
=======

Logging is the practice of emitting log messages that describe what is happening in the
system, or "events" in short. Log events can have varying degrees of severity, such as
``debug``, ``info``, ``warning``, ``error`` or even ``critical``. By default, Open Klant
emits logs with level ``info`` and higher.

A collection of log events with a correlation ID (like a request or trace ID) allow one
to reconstruct the chain of events that took place which lead to a particular outcome.

Open Klant emits structured logs in JSON format (unless explicitly configured otherwise),
which should make log aggregation and analysis easier.

We try to keep a consistent log message structure, where the following keys
are (usually) present:

``source``
    The component in the application stack that produced the log entry. Typical
    values are ``uwsgi`` and ``app``.

``level``
    The severity level of the log message. One of ``debug``, ``info``, ``warning``,
    ``error`` or ``critical``.

``timestamp``
    The moment when the log entry was produced, a string in ISO-8601 format. Most of
    the logs have microsecond precision, but some of them are limited to second
    precision.

``event``
    The event that occurred, e.g. ``request_started`` or ``spawned worker (PID 123)``.
    This gives the semantic meaning to the log entry.

Other keys that frequently occur are:

``request_id``
    Present for application logs emitted during an HTTP request, makes it possible to
    correlate multiple log entries for a single request. Not available in logs emitted
    by background tasks or logs emitted before/after the Open Klant app.

.. tip:: Certain log aggregation solutions require you to configure "labels" to extract
   for efficient querying. You can use the above summary of log context keys to configure
   this according to your needs.

.. note:: We can not 100% guarantee that every log message will always be JSON due to
   limitations in third party software/packages that we use. Most (if not all) log
   aggregation technologies support handling both structured and unstructured logs.


.. _installation_observability_metrics:

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

Generic
-------

``http.server.duration``
    Captures how long each HTTP request took, in ms. The metric produces histogram data.

``http.server.request.duration`` (not active)
    The future replacement of ``http.server.duration``, in seconds. Currently not
    enabled, but the code is in the Open Telemetry SDK instrumentation already and could
    possibly be opted-in to.

Application specific
--------------------

Accounts
^^^^^^^^

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

Tracing
=======

.. note:: A vendor-agnostic implementation is under development. Currently you can
   already use Elastic APM.

Tracing makes it possible to follow the flow of requests across system boundaries,
e.g. from one application to another. This makes it possible to pinpoint where errors
or performance degrations are situated exactly. Trace IDs also make it possible to
correlate the relevant log entries.

.. note:: Better support for (distributed) traces is underway.

Error monitoring
================

Uncaught exceptions are automatically sent to Sentry, if configured. It's highly
recommended to configure Sentry for proper insight into bugs.

.. _installation_observability_otel_config:

Open Telemetry Configuration
============================

You should be able to use the standard Open Telemetry
`environment variables <https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/>`_,
but we highlight some that you'd commonly want to specify for typical use cases.

Disabling Open Telemetry
------------------------

Set ``OTEL_SDK_DISABLED=true`` to disable telemetry entirely. This does not affect the
(structured) logging to the container stdout/stderr.

Configuring the Open Telemetry sink
-----------------------------------

Enabling Open Telemetry (enabled by default) requires you to have a "sink" to push the
telemetry data to. Open Klant only supports the Open Telemetry Protocol (OTLP). You can
use any vendor that supports this protocol (over gRPC or HTTP/protobuf).

.. tip:: We recommend the usage of the Open Telemetry
   `Collector <https://opentelemetry.io/docs/collector/>`_ as sink - you are then in
   full control of how telemetry is processed and exported.

**Environment variables you likely want to set**

* ``OTEL_EXPORTER_OTLP_ENDPOINT``: network address where to send the metrics to. Examples
  are: ``https://otel.example.com:4318`` or ``http://otel-collector.namespace.cluster.svc:4317``.
  It defaults to ``localhost:4317``, which will **not** work in a container context.

* ``OTEL_EXPORTER_OTLP_METRICS_INSECURE``: set to ``true`` if the endoint is not protected
  with TLS.

* ``OTEL_EXPORTER_OTLP_HEADERS``: Any additional HTTP headers, e.g. when your collector
  is username/password protected with Basic auth, you want something like:
  ``Authorization=Basic <base64-username-colon-password>``.

* ``OTEL_EXPORTER_OTLP_PROTOCOL``: controls the wire protocol for the OTLP data. Defaults to
  ``grpc``. Available options: ``grpc`` and ``http/protobuf``.

* ``OTEL_METRIC_EXPORT_INTERVAL``: controls how often (in milliseconds) the metrics are
  exported. The exports run in a background thread and should not affect the performance
  of the application. The default is every minute (``60000``).

* ``_OTEL_ENABLE_CONTAINER_RESOURCE_DETECTOR=true``: enable this when not deploying on
  Kubernetes, but in another container runtime like Docker or Podman.

  .. tip:: On Kubernetes, use the Collector
     `attributes processor <https://opentelemetry.io/docs/platforms/kubernetes/collector/components/#kubernetes-attributes-processor>`_.
