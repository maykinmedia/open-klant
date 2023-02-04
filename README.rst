==========
Open Klant
==========

:Version: 0.1.0
:Source: https://bitbucket.org/maykinmedia/openklant
:Keywords: ``klanten``, ``contactmomenten``, ``API``, ``Common Ground``
:License: EUPL
:PythonVersion: 3.8

|build-status| |requirements|

Project dat de `Klanten API` | https://klanten-api.vng.cloud en `Contactmomenten API` | https://contactmomenten-api.vng.cloud/ in een enkel component combineert.

Ontwikkeld door `Maykin Media B.V.`_ voor de gemeente Den Haag


Introductie
============

Open Klant biedt de volgende APIs aan:

 * Klanten API
 * Contactmomenten API

Deze APIs zijn door de VNG grotendeels gestandaardiseerd in het kader van de Zaakgericht Werken APIs, echter zijn niet opgenomen in de definitieve ZGW API scope ( https://vng.nl/projecten/zaakgericht-werken-api ) en zijn dus aangrenzende APIs die naast de ZGW APIs kunnen worden ingezet.

Doel en functionaliteiten
=========================

Doel van Open Klant is het bieden van 1 centrale registratieplaats van klantgegevens (inwoner/bedrijf) en contactmomenten van een gemeente. Hiermee worden verdubbelingen qua registratie voorkomen en kan er vanuit andere applicaties inzicht gegeven in welke berichten naar welke klanten zijn gestuurd.

Open Klant heeft vergeleken met de referentiecomponenten een aantal uitbreidingen gekregen, zoals het inloggen via SSO/OIDC en integratie met Open Notificaties.

Open Klant biedt momenteel nog geen automatische BRP (Haal Centraal) integratie: de aanroepende applicaties zijn verantwoordelijk voor het invoeren en waar nodig bijwerken van de klantgegevens.

Open Klant biedt momenteel geen eigen klantnotificatie functionaliteit: de Contactmomenten API is voor het registreren door een vakapplicatie van bijvoorbeeld een emailbericht wat naar een bepaalde klant is gestuurd.

Open Klant biedt momenteel geen integratie met Open Zaak. Een aanroepende applicatie is verantwoordelijk voor het leggen van de juiste verwijzingen in Open Zaak naar de Open Klant APIs en het onderhouden van de verwijzingen.

Relatie met de VNG Klanten API en Contactmomenten API
=====================================================

Open Klant is een 'friendly fork' van beide referentiecomponenten. De API is op enkele punten uitgebreid met additionele velden, die expliciet als 'AFWIJKING' zijn gemarkeerd in de OAS. Bij de inzet van Open Klant wordt zoveel mogelijk vastgehouden aan de specificatie en werking van de VNG APIs.

Ondersteuning en ontwikkeling
=============================

Dit component wordt momenteel alleen ingezet en doorontwikkeld voor gemeente Den Haag. Inzet door derden is conform de licentie toegestaan echter as-is en zonder ondersteuning, voor vragen over doorontwikkelingen en/of een supportovereenkomst kan contact opgenomen worden met Maykin. Beantwoording van issues in Github wordt overgelaten aan de community.

Documentatie
=============

See ``INSTALL.rst`` for installation instructions, available settings and
commands.


References
==========

.. _Maykin Media B.V.: https://www.maykinmedia.nl
