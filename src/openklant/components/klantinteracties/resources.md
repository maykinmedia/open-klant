# Resources

Dit document beschrijft de (RGBZ-)objecttypen die als resources ontsloten
worden met de beschikbare attributen.


## Actor

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/actor)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| uuid | Unieke (technische) identificatiecode van de actor. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| naam | Naam van de actor. | string | ja | C​R​U​D |
| soortActor | Geeft aan van welke specifieke soort actor sprake is. | string | ja | C​R​U​D |
| indicatieActief | Geeft aan of aan de actor nog betrokken mag worden bij nieuwe klantcontacten. Voor niet-actieve is dit niet toegestaan. | boolean | nee | C​R​U​D |

## Medewerker

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/medewerker)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| functie | Functie van de geautomatiseerde actor of beschrijving van de werkzaamheden die deze uitvoert. | string | ja | C​R​U​D |
| emailadres | Elektronisch postadres waaronder de MEDEWERKER in de regel bereikbaar is. | string | nee | C​R​U​D |
| telefoonnummer | Telefoonnummer waaronder de MEDEWERKER in de regel bereikbaar is. | string | ja | C​R​U​D |

## GeautomatiseerdeActor

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/geautomatiseerdeactor)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| functie | Functie van de geautomatiseerde actor of beschrijving van de werkzaamheden die deze uitvoert. | string | ja | C​R​U​D |
| omschrijving | Omschrijving van de geautomatiseerde actor. | string | nee | C​R​U​D |

## OrganisatorischeEenheid

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/organisatorischeeenheid)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| omschrijving | Omschrijving van de geautomatiseerde actor. | string | nee | C​R​U​D |
| emailadres | Elektronisch postadres waaronder de MEDEWERKER in de regel bereikbaar is. | string | nee | C​R​U​D |
| faxnummer | Faxnummer waaronder de organisatorische eenheid in de regel bereikbaar is. | string | ja | C​R​U​D |
| telefoonnummer | Telefoonnummer waaronder de MEDEWERKER in de regel bereikbaar is. | string | ja | C​R​U​D |

## Betrokkene

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/betrokkene)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| uuid | Unieke (technische) identificatiecode van de betrokkene bij klantcontact. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| digitaleAdressen | Digitale adressen van de betrokkene bij klantcontact. | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| rol | Rol die de betrokkene bij klantcontact tijdens dat contact vervulde. | string | ja | C​R​U​D |
| organisatienaam | Naam van de organisatie waarmee de betrokkene bij klantcontact een relatie had. | string | nee | C​R​U​D |
| initiator |  | boolean | ja | C​R​U​D |

## Bijlage

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/bijlage)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| uuid | Unieke (technische) identificatiecode van het inhoudsdeel. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |

## DigitaalAdres

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/digitaaladres)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| uuid | Unieke (technische) identificatiecode van het digitaal adres. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| adres | Digitaal adres waarmee een persoon of organisatie bereikt kan worden. | string | ja | C​R​U​D |
| soortDigitaalAdres | Typering van het digitale adres die aangeeft via welk(e) kanaal of kanalen met dit adres contact kan worden opgenomen. | string | ja | C​R​U​D |
| omschrijving | Omschrijving van het digitaal adres. | string | ja | C​R​U​D |

## InterneTaak

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/internetaak)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| uuid | Unieke (technische) identificatiecode van de interne taak. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| nummer | Uniek identificerend nummer dat tijdens communicatie tussen mensen kan worden gebruikt om de specifieke interne taak aan te duiden. | string | ja | C​R​U​D |
| gevraagdeHandeling | Handeling die moet worden uitgevoerd om de taak af te ronden. | string | ja | C​R​U​D |
| toelichting | Toelichting die, aanvullend bij de inhoud van het klantcontact dat aanleiding gaf tot de taak en de gevraagde handeling, bijdraagt aan het kunnen afhandelen van de taak. | string | nee | C​R​U​D |
| status | Aanduiding van de vordering bij afhandeling van de interne taak. | string | ja | C​R​U​D |
| toegewezenOp | Datum en tijdstip waarop de interne taak aan een actor werd toegewezen. | string | nee | ~~C~~​R​~~U~~​~~D~~ |

## Klantcontact

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/klantcontact)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| uuid | Unieke (technische) identificatiecode van de betrokkene bij klantcontact. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| gingOverOnderwerpobjecten | Onderwerpobject dat tijdens een klantcontact aan de orde was. | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| omvatteBijlagen | Bijlage die (een deel van) de inhoud van het klantcontact beschrijft. | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| hadBetrokkenen | Persoon of organisatie die betrokken was bij een klantcontact. | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| leiddeTotInterneTaken | Klantcontact dat leidde tot een interne taak. | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| nummer | Uniek identificerend nummer dat tijdens communicatie tussen mensen kan worden gebruikt om het specifieke klantcontact aan te duiden. | string | ja | C​R​U​D |
| kanaal | Communicatiekanaal dat bij het klantcontact werd gebruikt. | string | ja | C​R​U​D |
| onderwerp | Datgene waarover het klantcontact ging. | string | ja | C​R​U​D |
| hadBetrokkenActoren | Actor die bij een klantcontact betrokken was. | array | ja | C​R​U​D |
| inhoud | Informatie die tijdens het klantcontact werd overgebracht of uitgewisseld, voor zover die voor betrokkenen of actoren relevant is. | string | nee | C​R​U​D |
| indicatieContactGelukt | Geeft, indien bekend, aan of de poging contact tussen de gemeente en inwoner(s) of organisatie(s) tot stand te brengen succesvol was. | boolean | nee | C​R​U​D |
| taal | Taal, in ISO 639-2/B formaat, waarin de partij bij voorkeur contact heeft met de gemeente. Voorbeeld: nld. Zie: https://www.iso.org/standard/4767.html | string | ja | C​R​U​D |
| vertrouwelijk | Geeft aan of onderwerp, inhoud en kenmerken van het klantcontact vertrouwelijk moeten worden behandeld. | boolean | ja | C​R​U​D |
| plaatsgevondenOp | Datum en tijdstip waarop het klantontact plaatsvond. Als het klantcontact een gesprek betrof, is dit het moment waarop het gesprek begon. Als het klantcontact verzending of ontvangst van informatie betrof, is dit bij benadering het moment waarop informatie door gemeente verzonden of ontvangen werd. | string | nee | C​R​U​D |

## Onderwerpobject

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/onderwerpobject)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| uuid | Unieke (technische) identificatiecode van het onderwerpdeel. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |

## PartijIdentificator

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/partijidentificator)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| uuid | Unieke (technische) identificatiecode van de partij-identificator. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| anderePartijIdentificator | Vrij tekstveld om de verwijzing naar een niet-voorgedefinieerd objecttype, soort objectID of Register vast te leggen.  | string | nee | C​R​U​D |

## Partij

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/partij)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| uuid | Unieke (technische) identificatiecode van de partij. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| nummer | Uniek identificerend nummer dat tijdens communicatie tussen mensen kan worden gebruikt om de specifieke partij aan te duiden. | string | ja | C​R​U​D |
| interneNotitie | Mededelingen, aantekeningen of bijzonderheden over de partij, bedoeld voor intern gebruik. | string | nee | C​R​U​D |
| betrokkenen | Betrokkene bij klantcontact die een partij was. | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| digitaleAdressen | Digitaal adres dat een partij verstrekte voor gebruik bij toekomstig contact met de gemeente. | array | ja | C​R​U​D |
| vertegenwoordigde | Partij die een andere partij vertegenwoordigde. | array | ja | C​R​U​D |
| partijIdentificatoren | Partij-identificatoren die hoorde bij deze partij. | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| soortPartij | Geeft aan van welke specifieke soort partij sprake is. | string | ja | C​R​U​D |
| indicatieGeheimhouding | Geeft aan of de verstrekker van partijgegevens heeft aangegeven dat deze gegevens als geheim beschouwd moeten worden. | boolean | ja | C​R​U​D |
| voorkeurstaal | Taal, in ISO 639-2/B formaat, waarin de partij bij voorkeur contact heeft met de gemeente. Voorbeeld: nld. Zie: https://www.iso.org/standard/4767.html | string | nee | C​R​U​D |
| indicatieActief | Geeft aan of de contactgegevens van de partij nog gebruikt morgen worden om contact op te nemen. Gegevens van niet-actieve partijen mogen hiervoor niet worden gebruikt. | boolean | ja | C​R​U​D |

## Contactpersoon

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/contactpersoon)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| uuid | Unieke (technische) identificatiecode van de contactpersoon. | string | nee | C​R​U​D |

## Persoon

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/persoon)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |

## Organisatie

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/organisatie)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| naam | Naam van de organisatie. | string | nee | C​R​U​D |


* Create, Read, Update, Delete
