==========
Open Klant
==========

:Version: 0.5.0-pre
:Source: https://github.com/maykinmedia/open-klant
:Keywords: klanten, klantinteracties, contactmomenten, api, common ground
:License: EUPL

|docs| |docker|

Registratiecomponent voor de opslag en ontsluiting van klantgegevens volgens de
Klantinteracties API-specificatie. (`English version`_)

Ontwikkeld door `Maykin B.V.`_ in opdracht van de gemeente Den Haag.


Introductie
===========

Open Klant implementeert de (concept) `Klantinteracties API`_ specificatie van 
`VNG`_ welke een beperkte set aan gegevens over klanten en hun interactie met
de gemeente kan opslaan en ontsluiten.

Samen met gemeenten, die volop bezig zijn met de implementatie van Common 
Ground, en VNG, wordt gewerkt aan standaardisatie van de API en realisatie van 
Open Klant als beproeving van de toekomstige API standaard.


API specificatie
================

==============  ==============  =============================
Versie          Release datum   API specificatie
==============  ==============  =============================
latest          n/a             t.b.d.

0.5-pre         2023-08-05      Klanten:
                                `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/v0.5-pre/src/openklant/components/klanten/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/v0.5-pre/src/openklant/components/klanten/openapi.yaml>`_
                                Contactmomenten:
                                `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/v0.5-pre/src/openklant/components/contactmomenten/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/v0.5-pre/src/openklant/components/contactmomenten/openapi.yaml>`_
==============  ==============  =============================

Vorige versies worden nog 6 maanden ondersteund nadat de volgende versie is 
uitgebracht. Versie 0.5-pre bevat nog de Klanten en Contactmomenten 
API-specificatie die door VNG is geschrapt en beschouwd moet worden als legacy.

Zie: `Alle versies en wijzigingen <https://github.com/maykinmedia/open-klant/blob/master/CHANGELOG.rst>`_


Ready-to-go implementatie
=========================

|build-status| |coverage| |code-style| |codeql| |black| |python-versions|

Deze implementatie is bedoeld als referentie implementatie van de API 
specificaties maar tevens een productiewaardig component dat ingezet kan worden
in het gemeentelijke ICT landschap.

Quickstart
----------

1. Download en start Open Klant:

   .. code:: bash

      $ wget https://raw.githubusercontent.com/maykinmedia/open-klant/master/docker-compose-quickstart.yml -O docker-compose.yml
      $ docker-compose -f docker-compose-qs.yml up -d
      $ docker-compose exec web src/manage.py loaddata demodata
      $ docker-compose exec web src/manage.py createsuperuser

2. In de browser, navigeer naar ``http://localhost:8000/`` om de beheerinterface
   en de API te benaderen.


Links
=====

* `Documentatie <https://open-klant.readthedocs.io/>`_
* `Docker image <https://hub.docker.com/r/maykinmedia/open-klant>`_
* `Issues <https://github.com/maykinmedia/open-klant/open-klant>`_
* `Code <https://github.com/maykinmedia/open-klant>`_
* `Community <https://commonground.nl/groups/view/6bca7599-0f58-44e4-a405-7aa3a4c682f3/open-klant>`_


Licentie
========

Copyright © Maykin B.V., 2023

Licensed under the EUPL_


.. _`English version`: README.EN.rst

.. _`Maykin B.V.`: https://www.maykinmedia.nl

.. _`Klantinteracties API`: https://vng-realisatie.github.io/klantinteracties/

.. _`VNG`: https://vng.nl/

.. _`EUPL`: LICENSE.md

.. |build-status| image:: https://github.com/maykinmedia/open-klant/actions/workflows/ci.yml/badge.svg?branch=master
    :alt: Build status
    :target: https://github.com/maykinmedia/open-klant/actions?query=workflow%3Aci

.. |docs| image:: https://readthedocs.org/projects/open-klant/badge/?version=latest
    :target: https://open-klant.readthedocs.io/
    :alt: Documentation Status

.. |coverage| image:: https://codecov.io/github/maykinmedia/open-klant/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage
    :target: https://codecov.io/gh/maykinmedia/open-klant

.. |code-style| image:: https://github.com/maykinmedia/open-klant/actions/workflows/code-style.yml/badge.svg?branch=master
    :alt: Code style
    :target: https://github.com/maykinmedia/open-klant/actions/workflows/code-style.yml

.. |codeql| image:: https://github.com/maykinmedia/open-klant/actions/workflows/codeql.yml/badge.svg?branch=master
    :alt: CodeQL scan
    :target: https://github.com/maykinmedia/open-klant/actions/workflows/codeql.yml

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style
    :target: https://github.com/psf/black

.. |docker| image:: https://img.shields.io/docker/v/maykinmedia/open-klant?sort=semver
    :alt: Docker image
    :target: https://hub.docker.com/r/maykinmedia/open-klant

.. |python-versions| image:: https://img.shields.io/badge/python-3.11%2B-blue.svg
    :alt: Supported Python version

.. |lint-oas| image:: https://github.com/maykinmedia/open-klant/workflows/actions/lint-oas/badge.svg
    :alt: Lint OAS
    :target: https://github.com/maykinmedia/open-klant/actions?query=workflow%3Alint-oas

.. |generate-sdks| image:: https://github.com/maykinmedia/open-klant/workflows/actions/generate-sdks/badge.svg
    :alt: Generate SDKs
    :target: https://github.com/maykinmedia/open-klant/actions?query=workflow%3Agenerate-sdks

.. |generate-postman-collection| image:: https://github.com/maykinmedia/open-klant/workflows/actions/generate-postman-collection/badge.svg
    :alt: Generate Postman collection
    :target: https://github.com/maykinmedia/open-klant/actions?query=workflow%3Agenerate-postman-collection

