.. _installation_observability_logging:

=======
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


