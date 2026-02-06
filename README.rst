==========
Open Klant
==========

:Version: 2.15.0
:Source: https://github.com/maykinmedia/open-klant
:Keywords: klanten, klantinteracties, contactgegevens, api, common ground
:License: EUPL

|docs| |docker|

Registratiecomponent voor de opslag en ontsluiting van klantgegevens volgens de
Klantinteracties en Contactgegevens API-specificaties.

Ontwikkeld door `Maykin B.V.`_ in samenwerking met gemeente Amsterdam, gemeente
Den Haag, gemeente Utrecht en VNG Realisatie.


Introductie
===========

Open Klant implementeert 2 APIs: Klantinteracties API en Contactgegevens API.
De `Klantinteracties API`_  is gebaseerd op de specificatie van
`VNG`_ welke een beperkte set aan gegevens over klanten en hun interactie met
de gemeente kan opslaan en ontsluiten.
De Contactgegevens API is een unieke API die niet op een standaard is gebaseerd.

Samen met gemeenten, die volop bezig zijn met de implementatie van Common
Ground, en VNG, wordt gewerkt aan standaardisatie van de API en realisatie van
Open Klant als beproeving van de toekomstige API standaard.


API specificatie
================

Hieronder staat de laatste versie van Open Klant en welke versie van de
API-specificaties wordt aangeboden.

==================  =========================  =============   ================
Open Klant versie   API versie                 Release datum   API specificatie
==================  =========================  =============   ================
master/latest       n/a                        n/a             | Klantinteracties:
                                                                 `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/master/src/openklant/components/klantinteracties/openapi.yaml>`_,
                                                                 `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/master/src/openklant/components/klantinteracties/openapi.yaml>`_,
                                                                 (`diff <https://github.com/maykinmedia/open-klant/compare/2.15.0..master>`_)
                                                               | Contactgegevens:
                                                                 `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/master/src/openklant/components/contactgegevens/openapi.yaml>`_,
                                                                 `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/master/src/openklant/components/contactgegevens/openapi.yaml>`_,
                                                                 (`diff <https://github.com/maykinmedia/open-klant/compare/2.15.0..master>`_)
2.15.0              | Klantinteracties: 0.6.0  2026-02-06      | Klantinteracties:
                    | Contactgegevens: 1.1.1                     `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/2.15.0/src/openklant/components/klantinteracties/openapi.yaml>`_,
                                                                 `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/2.15.0/src/openklant/components/klantinteracties/openapi.yaml>`_,
                                                                 (`diff <https://github.com/maykinmedia/open-klant/compare/2.14.0..2.15.0>`_)
                                                               | Contactgegevens:
                                                                 `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/2.15.0/src/openklant/components/contactgegevens/openapi.yaml>`_,
                                                                 `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/open-klant/2.15.0/src/openklant/components/contactgegevens/openapi.yaml>`_,
                                                                 (`diff <https://github.com/maykinmedia/open-klant/compare/2.14.0..2.15.0>`_)
==================  =========================  =============   ================

Vorige versies worden nog 6 maanden ondersteund nadat de volgende versie is
uitgebracht. Open Klant versie 1.0.0 bevat nog de Klanten en Contactmomenten
API-specificatie die door VNG is geschrapt en beschouwd moet worden als legacy.

Zie: `Alle versies en wijzigingen <https://github.com/maykinmedia/open-klant/blob/master/CHANGELOG.rst>`_


Semantisch Informatiemodel
==========================
.. image:: https://raw.githubusercontent.com/maykinmedia/open-klant/refs/heads/master/docs/OpenKlant2SIM.drawio-v2.png
   :width: 800px

Opmerkingen
-----------
Bovenstaand informatiemodel is opgesteld met de volgende opmerkingen:

 * Voor de leesbaarheid en onderhoudbaarheid bevat het SIM niet de attributen zoals in het oorspronkelijke model. Deze zijn niet belangrijk voor het begrip van het model en eenvoudig op te zoeken in de API-specificatie.
 * Voor de relaties tussen entiteiten worden de feitelijke attribuutnamen uit de API specificatie gebruikt met weglating van de entiteit waarnaar wordt verwezen, bijv. "leiddeTotInterneTaken" word "leidde tot".Dit verbetert de de relatie met de API en daarmee het begrip. Als er geen betekenisvolle attribuutnaam voor de relatie wordt gebruikt (bijv. alleen de naam van de gerelateerde entiteit), is de relatienaam leeg gelaten.
 * Alle relaties tussen entiteiten worden gevisualiseerd. Soms zijn er relaties in beide richtingen.
 * De meeste API resources worden gevisualiseerd als een entiteit in het model. Actor Klantcontacten is weggelaten omdat dit een linktabel is.
 * Het kader “OpenKlant begrenzing“ geeft aan welke entiteiten in het register kunnen worden beheerd. De geel gekleurde entiteiten staan in een extern register. Om naar deze externe entiteiten te verwijzen wordt gebruik gemaakt van zgn. identificatoren.
 * Cardinaliteit is met * aangegeven als er meer dan één entiteit gekoppeld kan worden.
 * Bij Actor en Partij is class inheritance gebruikt om specieke actoren c.q. partijen te modelleren. Dit is in de API uitgewerkt met een attribuut soortActor en soortPartij die de specialisatie uitdrukt.


Ready-to-go implementatie
=========================

|build-status| |coverage| |code-style| |codeql| |ruff| |python-versions|

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

.. |code-style| image:: https://github.com/maykinmedia/open-klant/actions/workflows/code-quality.yml/badge.svg?branch=master
    :alt: Code style
    :target: https://github.com/maykinmedia/open-klant/actions/workflows/code-quality.yml

.. |codeql| image:: https://github.com/maykinmedia/open-klant/actions/workflows/code-analysis.yml/badge.svg?branch=master
    :alt: CodeQL scan
    :target: https://github.com/maykinmedia/open-klant/actions/workflows/code-analysis.yml

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. |docker| image:: https://img.shields.io/docker/v/maykinmedia/open-klant?sort=semver
    :alt: Docker image
    :target: https://hub.docker.com/r/maykinmedia/open-klant

.. |python-versions| image:: https://img.shields.io/badge/python-3.12%2B-blue.svg
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

