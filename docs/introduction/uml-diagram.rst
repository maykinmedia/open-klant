.. _uml_diagrams:

UML Diagrams
============

This section contains UML diagrams for resources per components.

.. note::

    These are the underlying data models and this shows the relationships between the resources,
    but not all attributes are the exact same as in the API. (e.g. the diagram for Organisatie shows fields like ``adres_huisnummer``,
    but in the API this is a nested field ``adres.huisnummer``)

.. uml_images::
    :apps: klantinteracties contactgegevens
    :excluded_models: AdresMixin ContactnaamMixin CorrespondentieadresMixin BezoekadresMixin
