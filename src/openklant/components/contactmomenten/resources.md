# Resources

Dit document beschrijft de (RGBZ-)objecttypen die als resources ontsloten
worden met de beschikbare attributen.


## Medewerker

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/medewerker)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| identificatie | Een korte unieke aanduiding van de MEDEWERKER. | string | nee | C​R​U​D |
| achternaam | De achternaam zoals de MEDEWERKER die in het dagelijkse verkeer gebruikt. | string | nee | C​R​U​D |
| voorletters | De verzameling letters die gevormd wordt door de eerste letter van alle in volgorde voorkomende voornamen. | string | nee | C​R​U​D |
| voorvoegselAchternaam | Dat deel van de geslachtsnaam dat voorkomt in Tabel 36 (GBA), voorvoegseltabel, en door een spatie van de geslachtsnaam is | string | nee | C​R​U​D |

## ContactMoment

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/contactmoment)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| vorigContactmoment | URL-referentie naar het vorige CONTACTMOMENT. | string | nee | C​R​U​D |
| volgendContactmoment | URL-referentie naar het volgende CONTACTMOMENT. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| bronorganisatie | Het RSIN van de Niet-natuurlijk persoon zijnde de organisatie die de klantinteractie heeft gecreeerd. Dit moet een geldig RSIN zijn van 9 nummers en voldoen aan https://nl.wikipedia.org/wiki/Burgerservicenummer#11-proef | string | ja | C​R​U​D |
| registratiedatum | De datum en het tijdstip waarop het CONTACTMOMENT is geregistreerd. | string | nee | C​R​U​D |
| kanaal | Het communicatiekanaal waarlangs het CONTACTMOMENT gevoerd wordt | string | nee | C​R​U​D |
| voorkeurskanaal | Het communicatiekanaal dat voor opvolging van de klantinteractie de voorkeur heeft van de KLANT. | string | nee | C​R​U​D |
| voorkeurstaal | Een ISO 639-2/B taalcode waarin de inhoud van het INFORMATIEOBJECT is vastgelegd. Voorbeeld: `nld`. Zie: https://www.iso.org/standard/4767.html | string | nee | C​R​U​D |
| tekst | Een toelichting die inhoudelijk de klantinteractie van de klant beschrijft. | string | nee | C​R​U​D |
| onderwerpLinks | Eén of meerdere links naar een product, webpagina of andere entiteit zodat contactmomenten gegroepeerd kunnen worden op onderwerp. | array | nee | C​R​U​D |
| initiatiefnemer | De partij die het contact heeft geïnitieerd. | string | nee | C​R​U​D |
| medewerker | URL-referentie naar een medewerker | string | nee | C​R​U​D |

## AuditTrail

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/audittrail)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| uuid | Unieke identificatie van de audit regel. | string | nee | C​R​U​D |
| bron | De naam van het component waar de wijziging in is gedaan.

Uitleg bij mogelijke waarden:

* `ac` - Autorisaties API
* `nrc` - Notificaties API
* `zrc` - Zaken API
* `ztc` - Catalogi API
* `drc` - Documenten API
* `brc` - Besluiten API
* `cmc` - Contactmomenten API
* `kc` - Klanten API | string | ja | C​R​U​D |
| applicatieId | Unieke identificatie van de applicatie, binnen de organisatie. | string | nee | C​R​U​D |
| applicatieWeergave | Vriendelijke naam van de applicatie. | string | nee | C​R​U​D |
| gebruikersId | Unieke identificatie van de gebruiker die binnen de organisatie herleid kan worden naar een persoon. | string | nee | C​R​U​D |
| gebruikersWeergave | Vriendelijke naam van de gebruiker. | string | nee | C​R​U​D |
| actie | De uitgevoerde handeling.

De bekende waardes voor dit veld zijn hieronder aangegeven,                         maar andere waardes zijn ook toegestaan

Uitleg bij mogelijke waarden:

* `create` - Object aangemaakt
* `list` - Lijst van objecten opgehaald
* `retrieve` - Object opgehaald
* `destroy` - Object verwijderd
* `update` - Object bijgewerkt
* `partial_update` - Object deels bijgewerkt | string | ja | C​R​U​D |
| actieWeergave | Vriendelijke naam van de actie. | string | nee | C​R​U​D |
| resultaat | HTTP status code van de API response van de uitgevoerde handeling. | integer | ja | C​R​U​D |
| hoofdObject | De URL naar het hoofdobject van een component. | string | ja | C​R​U​D |
| resource | Het type resource waarop de actie gebeurde. | string | ja | C​R​U​D |
| resourceUrl | De URL naar het object. | string | ja | C​R​U​D |
| toelichting | Toelichting waarom de handeling is uitgevoerd. | string | nee | C​R​U​D |
| resourceWeergave | Vriendelijke identificatie van het object. | string | ja | C​R​U​D |
| aanmaakdatum | De datum waarop de handeling is gedaan. | string | nee | ~~C~~​R​~~U~~​~~D~~ |

## KlantContactMoment

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/klantcontactmoment)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| contactmoment | URL-referentie naar het CONTACTMOMENT. | string | ja | C​R​U​D |
| klant | URL-referentie naar de KLANT. | string | ja | C​R​U​D |
| rol | De rol van de KLANT in het CONTACTMOMENT. Indien de KLANT zowel gesprekspartner als belanghebbende is, dan worden er twee KLANTCONTACTMOMENTen aangemaakt. | string | ja | C​R​U​D |

## ObjectContactMoment

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/objectcontactmoment)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| contactmoment | URL-referentie naar het CONTACTMOMENT. | string | ja | C​R​U​D |
| object | URL-referentie naar het gerelateerde OBJECT (in een andere API). | string | ja | C​R​U​D |
| objectType | Het type van het gerelateerde OBJECT.

Uitleg bij mogelijke waarden:

* `zaak` - Zaak | string | ja | C​R​U​D |


* Create, Read, Update, Delete
