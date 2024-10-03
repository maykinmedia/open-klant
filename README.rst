==========
Open Klant
==========

:Version: 2.3.0
:Source: https://github.com/maykinmedia/open-klant
:Keywords: klanten, klantinteracties, contactmomenten, api, common ground
:License: EUPL

|docs| |docker|

Registratiecomponent voor de opslag en ontsluiting van klantgegevens volgens de
Klantinteracties API-specificatie. (`English version`_)

Ontwikkeld door `Maykin B.V.`_ in samenwerking met gemeente Amsterdam, gemeente 
Den Haag, gemeente Utrecht en VNG Realisatie.


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

Hieronder staat de versie van Open Klant en welke versie van de 
API-specificatie wordt aangeboden.

==================  ==============  =============   ================
Open Klant versie   API versie      Release datum   API specificatie
==================  ==============  =============   ================
master/latest       n/a             n/a             `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/master/src/openklant/components/klantinteracties/openapi.yaml>`_,
                                                    `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/master/src/openklant/components/klantinteracties/openapi.yaml>`_,
                                                    (`diff <https://github.com/maykinmedia/open-klant/compare/2.3.0..master#diff-0198a3368d5c8c5325ef11e3c0ba8d2986f50b964c8002d3ece7cadc0b8ba23d>`_)
2.3.0               0.0.3+          2024-09-05      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/2.3.0/src/openklant/components/klantinteracties/openapi.yaml>`_,
                                                    `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/2.3.0/src/openklant/components/klantinteracties/openapi.yaml>`_,
                                                    (`diff <https://github.com/maykinmedia/open-klant/compare/2.1.0..2.3.0#diff-0198a3368d5c8c5325ef11e3c0ba8d2986f50b964c8002d3ece7cadc0b8ba23d>`_)
2.1.0               0.0.3+          2024-07-16      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/2.1.0/src/openklant/components/klantinteracties/openapi.yaml>`_,
                                                    `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/2.1.0/src/openklant/components/klantinteracties/openapi.yaml>`_,
                                                    (`diff <https://github.com/maykinmedia/open-klant/compare/2.0.0..2.1.0#diff-0198a3368d5c8c5325ef11e3c0ba8d2986f50b964c8002d3ece7cadc0b8ba23d>`_)
2.0.0               0.0.3           2024-03-15      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/2.0.0/src/openklant/components/klantinteracties/openapi.yaml>`_,
                                                    `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/2.0.0/src/openklant/components/klantinteracties/openapi.yaml>`_
1.0.0               0.0.1           2023-08-05      Klanten:
                                                    `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/1.0.0/src/openklant/components/klanten/openapi.yaml>`_,
                                                    `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/1.0.0/src/openklant/components/klanten/openapi.yaml>`_
                                                    Contactmomenten:
                                                    `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/1.0.0/src/openklant/components/contactmomenten/openapi.yaml>`_,
                                                    `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/1.0.0/src/openklant/components/contactmomenten/openapi.yaml>`_
==================  ==============  =============   ================

Vorige versies worden nog 6 maanden ondersteund nadat de volgende versie is 
uitgebracht. Open Klant versie 1.0.0 bevat nog de Klanten en Contactmomenten 
API-specificatie die door VNG is geschrapt en beschouwd moet worden als legacy.

Zie: `Alle versies en wijzigingen <https://github.com/maykinmedia/open-klant/blob/master/CHANGELOG.rst>`_


Ready-to-go implementatie
=========================

|build-status| |coverage| |code-style| |codeql| |black| |python-versions|

Deze implementatie is bedoeld als referentie implementatie van de API 
specificaties maar tevens een productiewaardig component dat ingezet kan worden
in het ICT landschap van de overheid.

Quickstart
----------

1. Download en start Open Klant:

   .. code:: bash

      $ wget https://raw.githubusercontent.com/maykinmedia/open-klant/master/docker-compose.yml
      $ docker-compose up -d --no-build
      $ docker-compose exec web src/manage.py loaddata klantinteracties contactgegevens
      $ docker-compose exec web src/manage.py createsuperuser

2. In de browser, navigeer naar ``http://localhost:8000/`` om de beheerinterface
   en de API te benaderen.


Links
=====

* `Documentatie <https://open-klant.readthedocs.io/>`_
* `Docker image <https://hub.docker.com/r/maykinmedia/open-klant>`_
* `Issues <https://github.com/maykinmedia/open-klant/issues>`_
* `Code <https://github.com/maykinmedia/open-klant>`_
* `Community <https://commonground.nl/groups/view/6bca7599-0f58-44e4-a405-7aa3a4c682f3/open-klant>`_


Licentie
========

Copyright © Maykin B.V., 2023 - 2024

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

