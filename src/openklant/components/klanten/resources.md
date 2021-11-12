# Resources

Dit document beschrijft de (RGBZ-)objecttypen die als resources ontsloten
worden met de beschikbare attributen.


## KlantAdres

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/klantadres)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| straatnaam |  | string | nee | C​R​U​D |
| huisnummer |  | integer | nee | C​R​U​D |
| huisletter |  | string | nee | C​R​U​D |
| huisnummertoevoeging |  | string | nee | C​R​U​D |
| postcode |  | string | nee | C​R​U​D |
| woonplaatsnaam |  | string | nee | C​R​U​D |
| landcode | De code, behorende bij de landnaam, zoals opgenomen in de Land/Gebied-tabel van de BRP. | string | nee | C​R​U​D |

## Klant

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/klant)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| bronorganisatie | Het RSIN van de Niet-natuurlijk persoon zijnde de organisatie die de klant heeft gecreeerd. Dit moet een geldig RSIN zijn van 9 nummers en voldoen aan https://nl.wikipedia.org/wiki/Burgerservicenummer#11-proef | string | ja | C​R​U​D |
| klantnummer | De unieke identificatie van de klant binnen de bronorganisatie. | string | ja | C​R​U​D |
| bedrijfsnaam | De bedrijfsnaam van de klant. | string | nee | C​R​U​D |
| functie | De functie van de klant. | string | nee | C​R​U​D |
| websiteUrl | Het label of etiket dat aan de specifieke informatiebron, zoals een webpagina, een bestand of een plaatje op internet is toegewezen waar de KLANT in de regel op het internet vindbaar is. | string | ja | C​R​U​D |
| voornaam | De voornaam, voorletters of roepnaam van de klant. | string | nee | C​R​U​D |
| voorvoegselAchternaam | Het voorvoegsel van de achternaam van de klant. | string | nee | C​R​U​D |
| achternaam | De achternaam van de klant. | string | nee | C​R​U​D |
| telefoonnummer | Het mobiele of vaste telefoonnummer van de klant. | string | nee | C​R​U​D |
| emailadres | Het e-mail adres van de klant. | string | nee | C​R​U​D |
| subject | URL-referentie naar een subject | string | nee | C​R​U​D |
| subjectType | Type van de `subject`.

Uitleg bij mogelijke waarden:

* `natuurlijk_persoon` - Natuurlijk persoon
* `niet_natuurlijk_persoon` - Niet-natuurlijk persoon
* `vestiging` - Vestiging | string | nee | C​R​U​D |
| aanmaakkanaal | Het communicatiekanaal waarlangs de klant is aangemaakt. | string | nee | C​R​U​D |

## VerblijfsAdres

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/verblijfsadres)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| aoaIdentificatie | De unieke identificatie van het OBJECT | string | ja | C​R​U​D |
| wplWoonplaatsNaam |  | string | nee | C​R​U​D |
| gorOpenbareRuimteNaam | Een door het bevoegde gemeentelijke orgaan aan een OPENBARE RUIMTE toegekende benaming | string | ja | C​R​U​D |
| aoaPostcode |  | string | nee | C​R​U​D |
| aoaHuisnummer |  | integer | nee | C​R​U​D |
| aoaHuisletter |  | string | nee | C​R​U​D |
| aoaHuisnummertoevoeging |  | string | nee | C​R​U​D |
| inpLocatiebeschrijving |  | string | nee | C​R​U​D |

## SubVerblijfBuitenland

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/subverblijfbuitenland)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| lndLandcode | De code, behorende bij de landnaam, zoals opgenomen in de Land/Gebied-tabel van de BRP. | string | ja | C​R​U​D |
| lndLandnaam | De naam van het land, zoals opgenomen in de Land/Gebied-tabel van de BRP. | string | ja | C​R​U​D |
| subAdresBuitenland1 |  | string | nee | C​R​U​D |
| subAdresBuitenland2 |  | string | nee | C​R​U​D |
| subAdresBuitenland3 |  | string | nee | C​R​U​D |

## NatuurlijkPersoon

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/natuurlijkpersoon)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| inpBsn | Het burgerservicenummer, bedoeld in artikel 1.1 van de Wet algemene bepalingen burgerservicenummer. | string | nee | C​R​U​D |
| anpIdentificatie | Het door de gemeente uitgegeven unieke nummer voor een ANDER NATUURLIJK PERSOON | string | nee | C​R​U​D |
| inpANummer | Het administratienummer van de persoon, bedoeld in de Wet BRP | string | nee | C​R​U​D |
| geslachtsnaam | De stam van de geslachtsnaam. | string | nee | C​R​U​D |
| voorvoegselGeslachtsnaam |  | string | nee | C​R​U​D |
| voorletters | De verzameling letters die gevormd wordt door de eerste letter van alle in volgorde voorkomende voornamen. | string | nee | C​R​U​D |
| voornamen | Voornamen bij de naam die de persoon wenst te voeren. | string | nee | C​R​U​D |
| geslachtsaanduiding | Een aanduiding die aangeeft of de persoon een man of een vrouw is, of dat het geslacht nog onbekend is.

Uitleg bij mogelijke waarden:

* `m` - Man
* `v` - Vrouw
* `o` - Onbekend | string | nee | C​R​U​D |
| geboortedatum |  | string | nee | C​R​U​D |

## NietNatuurlijkPersoon

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/nietnatuurlijkpersoon)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| innNnpId | Het door een kamer toegekend uniek nummer voor de INGESCHREVEN NIET-NATUURLIJK PERSOON | string | nee | C​R​U​D |
| annIdentificatie | Het door de gemeente uitgegeven unieke nummer voor een ANDER NIET-NATUURLIJK PERSOON | string | nee | C​R​U​D |
| statutaireNaam | Naam van de niet-natuurlijke persoon zoals deze is vastgelegd in de statuten (rechtspersoon) of in de vennootschapsovereenkomst is overeengekomen (Vennootschap onder firma of Commanditaire vennootschap). | string | nee | C​R​U​D |
| innRechtsvorm | De juridische vorm van de NIET-NATUURLIJK PERSOON. | string | nee | C​R​U​D |
| bezoekadres | De gegevens over het adres van de NIET-NATUURLIJK PERSOON | string | nee | C​R​U​D |

## Vestiging

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/vestiging)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| vestigingsNummer | Een korte unieke aanduiding van de Vestiging. | string | nee | C​R​U​D |
| handelsnaam | De naam van de vestiging waaronder gehandeld wordt. | array | nee | C​R​U​D |

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


* Create, Read, Update, Delete
